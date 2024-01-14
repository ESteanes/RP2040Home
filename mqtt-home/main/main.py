from .config_parsing.ConfigParser import ConfigParser
from .home_assistant.HomeAssistantMqttClient import HomeAssistantMqttClient


if __name__ == "__main__":
    myconfig = ConfigParser()
    myconfig.load("test-config.json")
    mydiscover = HomeAssistantMqttClient("UUID", myconfig.output_config)
    print(myconfig.wifi_config)
    print(myconfig.mqtt_config)
    print(mydiscover.haDiscoveryPayloads)
