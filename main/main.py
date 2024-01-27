from configparsing.configparser import ConfigParser
from homeassistant.homeassistantmqttclient import HomeAssistantMqttClient
import sys

if __name__ == "__main__":
    print(sys.path)
    myconfig = ConfigParser()
    myconfig.load("test-config.json")
    haMqttClient = HomeAssistantMqttClient("UUID", myconfig.output_config)
    haMqttClient.mqttInitialise(True)
    print(myconfig.wifi_config)
    print(myconfig.mqtt_config)
    print(haMqttClient.haDiscoveryPayloads)
