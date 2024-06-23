import unittest
from RP2040Home.configparsing.mqttconfig import MqttConfig
from RP2040Home.configparsing.homeassistantdiscoveryconfig import HomeAssistantDiscoveryConfig


class MqttConfig_Test(unittest.TestCase):

    def setUp(self):
        self.kwargs = {
            'host': 'test.mosquitto.org',
            'port': 1883,
            'user': 'mqttuser',
            'password': 'mqttpassword',
            'topic_prefix': 'home/assistant',
            'location': 'living room',
            'ha_discovery': {
                'enabled': "yes",
                'node_id': 'homeassistant'
            }
        }

    def test_standard_case(self):
        config = MqttConfig(**self.kwargs)
        self.assertEqual(config.host, 'test.mosquitto.org')
        self.assertEqual(config.port, 1883)
        self.assertEqual(config.user, 'mqttuser')
        self.assertEqual(config.password, 'mqttpassword')
        self.assertEqual(config.topic_prefix, 'home/assistant')
        self.assertEqual(config.location, 'living-room')
        self.assertIsInstance(config.ha_discovery, HomeAssistantDiscoveryConfig)
        self.assertTrue(config.ha_discovery.enabled)

    def test_missing_entries(self):
        incomplete_kwargs = self.kwargs.copy()
        incomplete_kwargs.pop("host")
        with self.assertRaises(AttributeError) as context:
            MqttConfig(**incomplete_kwargs)
        self.assertEqual(str(context.exception), "The attribute 'host' is missing - please check your configuration file")

    def test_unexpected_entries(self):
        extra_kwargs = self.kwargs.copy()
        extra_kwargs['another_key'] = "another value"
        config = MqttConfig(**extra_kwargs)
        self.assertEqual(config.host, 'test.mosquitto.org')
        self.assertEqual(config.port, 1883)
        self.assertEqual(config.user, 'mqttuser')
        self.assertEqual(config.password, 'mqttpassword')
        self.assertEqual(config.topic_prefix, 'home/assistant')
        self.assertEqual(config.location, 'living-room')
        self.assertIsInstance(config.ha_discovery, HomeAssistantDiscoveryConfig)
        self.assertTrue(config.ha_discovery.enabled)


if __name__ == '__main__':
    unittest.main()
