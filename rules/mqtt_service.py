"""MQTT integration layer for the controller role inside the rules app."""

from __future__ import annotations
from dataclasses import dataclass
import logging
from typing import Iterable

import paho.mqtt.client as mqtt

from devices.models import Device
from events.models import Event
from rules.models import Rule
from rules.parser import ParsedRule, parse_rule_text
from rules.engine import RuleEngine

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class RuleAction:
    topic: str
    payload: str
    device_id: str

class MQTTControllerService:
    def __init__(self, host: str, port: int, base_topic: str = "redes2/2311/04") -> None:
        self.host = host
        self.port = port
        self.base_topic = base_topic.rstrip("/")
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def connect(self) -> None:
        self.client.connect(self.host, self.port, keepalive=60)

    def start(self) -> None:
        self.connect()
        self.client.loop_forever()

    def stop(self) -> None:
        self.client.disconnect()

    def publish_device_action(self, topic: str, payload: str) -> None:
        self.client.publish(topic, payload)

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        logger.info("Conectado al broker MQTT con código %s", reason_code)
        client.subscribe(f"{self.base_topic}/#")

    def _on_message(self, client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8", errors="replace")
        
        if topic.endswith("/set"):
            return

        parts = topic.split("/")
        device_id = parts[-1]

        # VALIDACIÓN CRÍTICA: Solo procesamos si el dispositivo está registrado
        if not Device.objects.filter(device_id=device_id).exists():
            logger.warning("Mensaje ignorado de dispositivo no registrado: %s", device_id)
            return

        # Solo si está registrado creamos el evento en la BD
        event = Event.objects.create(
            device=device_id,
            value=payload,
            description="Evento MQTT recibido",
        )
        self.handle_event(event)

    def handle_event(self, event: Event) -> list[RuleAction]:
        # Ya sabemos que existe por el filtro en _on_message, pero lo recuperamos para actualizar estado
        device = Device.objects.get(device_id=event.device)
        device.current_state = event.value
        device.save(update_fields=["current_state"])

        rule_actions: list[RuleAction] = []
        for rule in self._matching_rules():
            parsed_rule = self._parse_rule(rule)
            if parsed_rule is None or parsed_rule.source_device != event.device:
                continue
            
            if RuleEngine.matches(parsed_rule, event.value):
                action = self._build_action(parsed_rule)
                rule_actions.append(action)
                self.publish_device_action(action.topic, action.payload)
                self._update_device_state(action.device_id, action.payload)
                event.description = f"Se ejecutó regla: {rule.raw_text}"
                event.save(update_fields=["description"])
                break

        return rule_actions

    def _matching_rules(self) -> Iterable[Rule]:
        return Rule.objects.filter(enabled=True)

    def _parse_rule(self, rule: Rule) -> ParsedRule | None:
        try:
            return parse_rule_text(rule.raw_text)
        except ValueError:
            return None

    def _build_action(self, rule: ParsedRule) -> RuleAction:
        topic = f"{self.base_topic}/{rule.action_device}/set"
        return RuleAction(topic=topic, payload=rule.action_value, device_id=rule.action_device)

    def _update_device_state(self, device_id: str, payload: str) -> None:
        try:
            device = Device.objects.get(device_id=device_id)
            device.current_state = payload
            device.save(update_fields=["current_state"])
        except Device.DoesNotExist:
            return