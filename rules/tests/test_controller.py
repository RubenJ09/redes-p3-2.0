from io import StringIO
from unittest.mock import patch, MagicMock
from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.core.management import call_command

from rules.models import Rule
from rules.parser import parse_rule_text
from rules.mqtt_service import MQTTControllerService
from devices.models import Device
from events.models import Event
from rules.engine import RuleEngine

class RuleEngineTests(SimpleTestCase):
    def test_engine_numeric_comparison(self):
        mock_rule = MagicMock(operator=">", threshold="25")
        self.assertTrue(RuleEngine.matches(mock_rule, "26"))
        self.assertFalse(RuleEngine.matches(mock_rule, "24"))

    def test_engine_equality_comparison(self):
        mock_rule = MagicMock(operator="==", threshold="ON")
        self.assertTrue(RuleEngine.matches(mock_rule, "ON"))
        self.assertFalse(RuleEngine.matches(mock_rule, "OFF"))

    def test_engine_invalid_data_handling(self):
        mock_rule = MagicMock(operator=">", threshold="25")
        self.assertFalse(RuleEngine.matches(mock_rule, "no_soy_un_numero"))

class RuleParserTests(SimpleTestCase):
    def test_rule_parsing_logic(self):
        parsed = parse_rule_text("si sensor_salon > 25 entonces switch_caldera OFF")
        self.assertEqual(parsed.source_device, "sensor_salon")
        self.assertEqual(parsed.operator, ">")
        self.assertEqual(parsed.threshold, "25")
        self.assertEqual(parsed.action_value, "OFF")

    def test_invalid_rule_raises_error(self):
        with self.assertRaises(ValueError):
            parse_rule_text("esto no es una regla")

class RunControllerCommandTests(TestCase):
    @patch("rules.management.commands.run_controller.MQTTControllerService.start")
    def test_run_controller_command_invokes_service(self, mocked_start):
        out = StringIO()
        call_command("run_controller", "--database", "db.sqlite3", stdout=out)
        self.assertIn("Controller iniciado", out.getvalue())
        mocked_start.assert_called_once()

class ControllerIntegrationTests(TestCase):
    def setUp(self):
        self.dev_sensor = Device.objects.create(
            device_id="sensor_salon",
            device_type=Device.DeviceType.SENSOR,
            topic="redes2/2311/04/sensor_salon"
        )
        self.dev_switch = Device.objects.create(
            device_id="switch_caldera",
            device_type=Device.DeviceType.SWITCH,
            topic="redes2/2311/04/switch_caldera",
            command_topic="redes2/2311/04/switch_caldera/set"
        )
        self.rule = Rule.objects.create(
            raw_text="si sensor_salon > 25 entonces switch_caldera OFF",
            enabled=True
        )
        self.service = MQTTControllerService("host", 1883)

    @patch("rules.mqtt_service.MQTTControllerService.publish_device_action")
    def test_controller_triggers_action_on_event(self, mock_publish):
        event = Event.objects.create(
            device="sensor_salon",
            value="26",
            description="Test"
        )

        actions = self.service.handle_event(event)

        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].payload, "OFF")
        self.assertEqual(actions[0].device_id, "switch_caldera")
        mock_publish.assert_called_with(
            "redes2/2311/04/switch_caldera/set", 
            "OFF"
        )

class RuleViewsTests(TestCase):
    def test_list_view_shows_rules(self):
        Rule.objects.create(raw_text="si s > 20 entonces d ON", enabled=True)
        response = self.client.get(reverse("rules:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "si s &gt; 20 entonces d ON")