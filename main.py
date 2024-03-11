from main.configparsing.configparser import ConfigParser
from main.homeassistant.homeassistantmqttclient import HomeAssistantMqttClient
import sys, network

if __name__ == "__main__":
    print(sys.path)
    myconfig = ConfigParser()
    myconfig.load("config.json")
    if network.WLAN(network.STA_IF).isconnected():
        haMqttClient = HomeAssistantMqttClient("UUID", myconfig)
        print(myconfig.wifi_config)
        print(myconfig.mqtt_config)
        print(haMqttClient.haDiscoveryPayloads)
        haMqttClient.mqttInitialise(True)
    else:
        print("Couldn't connect to any of the specified SSIDs, exiting")
    try:
        # while 1 and network.WLAN(network.STA_IF).isconnected():
        while 1:
            haMqttClient.mqtt_client.wait_msg()
    finally:
        haMqttClient.mqttStatus(False)
        haMqttClient.mqtt_client.disconnect()

