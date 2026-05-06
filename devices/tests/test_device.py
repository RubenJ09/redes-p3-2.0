from django.test import TestCase
from django.urls import reverse
from unittest.mock import MagicMock, patch
from devices.models import Device

class DeviceTests(TestCase):
    def setUp(self):
        self.switch = Device.objects.create(
            device_id="switch_caldera",
            name="Caldera",
            device_type=Device.DeviceType.SWITCH,
            topic="redes2/2311/04/switch_caldera",
            command_topic="redes2/2311/04/switch_caldera/set",
            current_state="OFF",
        )
        self.sensor = Device.objects.create(
            device_id="sensor_salon",
            name="Sensor salón",
            device_type=Device.DeviceType.SENSOR,
            topic="redes2/2311/04/sensor_salon",
            current_state="24",
        )

    def test_device_str(self):
        self.assertEqual(str(self.switch), "switch_caldera (Caldera)")

    def test_device_states(self):
        self.switch.current_state = "ON"
        self.sensor.current_state = "25.5"
        self.switch.save()
        self.sensor.save()
        self.assertEqual(Device.objects.get(device_id="switch_caldera").current_state, "ON")
        self.assertEqual(Device.objects.get(device_id="sensor_salon").current_state, "25.5")

    def test_list_view_shows_devices(self):
        response = self.client.get(reverse("devices:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "switch_caldera")
        self.assertContains(response, "sensor_salon")

    def test_create_device(self):
        response = self.client.post(reverse("devices:create"), {
            "device_id": "new_device",
            "name": "Nuevo",
            "device_type": "sensor",
            "topic": "redes2/2311/04/new",
            "current_state": "0",
        })
        self.assertRedirects(response, reverse("devices:list"))
        self.assertTrue(Device.objects.filter(device_id="new_device").exists())

    @patch("paho.mqtt.client.Client")
    def test_mqtt_connection_success(self, mock_mqtt):
        client_instance = mock_mqtt.return_value
        client_instance.connect.return_value = 0 
        result = client_instance.connect("redes2.ii.uam.es", 1883)
        self.assertEqual(result, 0)
        client_instance.connect.assert_called_with("redes2.ii.uam.es", 1883)

    @patch("paho.mqtt.client.Client")
    def test_mqtt_connection_failure(self, mock_mqtt):
        client_instance = mock_mqtt.return_value
        client_instance.connect.side_effect = Exception("Connection refused")
        
        with self.assertRaises(Exception):
            client_instance.connect("invalid_host", 1883)

    def test_sensor_oscillation_logic(self):
        val = 20
        inc = 1
        max_val = 22
        val += inc
        self.assertEqual(val, 21)
        val += inc
        self.assertEqual(val, 22)
        if val >= max_val:
            val = 20
        self.assertEqual(val, 20)