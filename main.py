from main.configparsing.configparser import ConfigParser
from main.homeassistant.homeassistantmqttclient import HomeAssistantMqttClient
import sys

if __name__ == "__main__":
    print(sys.path)
    myconfig = ConfigParser()
    myconfig.load("config.json")
    haMqttClient = HomeAssistantMqttClient("UUID", myconfig)
    print(myconfig.wifi_config)
    print(myconfig.mqtt_config)
    print(haMqttClient.haDiscoveryPayloads)
    haMqttClient.mqttInitialise(True)
    