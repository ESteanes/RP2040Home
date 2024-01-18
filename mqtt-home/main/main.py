from .config_parsing.ConfigParser import ConfigParser
from .home_assistant.HomeAssistantMqttClient import HomeAssistantMqttClient


if __name__ == "__main__":
    myconfig = ConfigParser()
    myconfig.load("test-config.json")
    haMqttClient = HomeAssistantMqttClient("UUID", myconfig.output_config)
    haMqttClient.mqttInitialise(True)
    print(myconfig.wifi_config)
    print(myconfig.mqtt_config)
    print(haMqttClient.haDiscoveryPayloads)
