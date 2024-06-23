import unittest
from RP2040Home.configparsing.configparser import ConfigParser
from RP2040Home.configparsing.mqttconfig import MqttConfig
from RP2040Home.configparsing.wificonfig import WifiConfig
from RP2040Home.configparsing.output import Output


class ConfigParser_Test(unittest.TestCase):
    def setUp(self):
        self.config_parser = ConfigParser()
        self.sample_data = {
            "pi": [
                {
                    "ssid": "ssid1",
                    "password": "password1"
                },
                {
                    "ssid": "ssid2",
                    "password": "password2"
                }
            ],
            "mqtt": {
                "host": "1.1.1.1",
                "port": "1883",
                "user": "",
                "password": "",
                "topic_prefix": "a_home_assistant_topic_prefix",
                "location": "a_client_location",
                "ha_discovery": {
                    "enabled": "yes",
                    "node_id": "a_node_id"
                }
            },
            "digital_outputs": [
                {
                    "output_type": "switch",
                    "name": "myOutput",
                    "pin": 17,
                    "on_payload": "ON",
                    "off_payload": "OFF"
                }
            ]
        }

    def test_parse_config(self):
        self.config_parser.load_from_object(self.sample_data)
        expected_mqtt_config = MqttConfig(
            host="1.1.1.1",
            port="1883",
            user="",
            password="",
            topic_prefix="a_home_assistant_topic_prefix",
            location="a_client_location",
            ha_discovery={
                "enabled": "yes",
                "node_id": "a_node_id"
                }
            )
        expected_wifi_config = []
        expected_wifi_config.append(WifiConfig("ssid1", "password1"))
        expected_wifi_config.append(WifiConfig("ssid2", "password2"))
        expected_output_config = [Output("switch", "myOutput", 17, "ON", "OFF")]
        self.assertEqual(self.config_parser.mqtt_config, expected_mqtt_config)
        self.assertEqual(self.config_parser.wifi_config, expected_wifi_config)
        self.assertEqual(self.config_parser.output_config, expected_output_config)
        return

    def test_validate_config_valid_pin(self):
        # GIVEN
        valid_output_config = [Output("switch", "myOutput", 17, "ON", "OFF")]
        allowed_pins = [0]
        # WHEN
        self.sample_data["digital_outputs"][0]["pin"] = 17
        with self.assertRaises(AttributeError) as context:
            self.config_parser.validate_config(self.sample_data, allowed_pins, valid_output_config)
        self.assertEqual(str(context.exception), "Output on 17 is not allowed, the only allowed GPIO pins are: 0")
        return

    def test_validate_config_no_outputs(self):
        self.sample_data["digital_outputs"] = []
        empty_output_config = []
        with self.assertRaises(ValueError) as context:
            self.config_parser.validate_config(self.sample_data, [0], empty_output_config)
        self.assertEqual(str(context.exception), "No output values are defined in config")
        return

    def test_validate_config_mismatched_outputs(self):
        empty_output_config = []
        allowed_pins = [17]
        with self.assertRaises(AttributeError) as context:
            self.config_parser.validate_config(self.sample_data, allowed_pins, empty_output_config)
        self.assertEqual(
            str(context.exception),
            "One or more outputs has been misconfigured, the only allowed GPIO pins are: "
            + ",".join(map(str, allowed_pins)))
        return


if __name__ == '__main__':
    unittest.main()
