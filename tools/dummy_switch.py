from __future__ import annotations

import argparse
import random
import time
import paho.mqtt.client as mqtt

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador de interruptor IoT")
    parser.add_argument("id", help="Identificador del dispositivo")
    parser.add_argument("--host", default="redes2.ii.uam.es", help="Host del broker")
    parser.add_argument("-p", "--port", type=int, default=1883, help="Puerto del broker")
    parser.add_argument("-P", "--probability", type=float, default=0.3, help="Probabilidad de fallo")
    parser.add_argument("--base-topic", default="redes2/2311/04", help="Prefijo del topic")
    return parser

def main() -> None:
    args = build_parser().parse_args()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    client.connect(args.host, args.port, keepalive=60)
    client.loop_start()

    topic = f"{args.base_topic}/{args.id}"
    command_topic = f"{topic}/set"
    state = "OFF"

    def on_message(client, userdata, message):
        nonlocal state
        desired = message.payload.decode("utf-8")
        if random.random() < args.probability:
            client.publish(topic, state)
            return
        if desired in {"ON", "OFF"}:
            state = desired
            client.publish(topic, state)

    client.subscribe(command_topic)
    client.on_message = on_message
    client.publish(topic, state)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()