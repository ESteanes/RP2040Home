from main.configparsing.configparser import ConfigParser
from main.homeassistant.payloadGenerator import PayloadGenerator
from main.homeassistant.mqttClient import MqttClient

import sys, network, machine
from umqtt.simple import MQTTClient

def main():
    led = machine.Pin("LED", machine.Pin.OUT)
    led.on()
    print(sys.path)
    myconfig = ConfigParser()
    myconfig.load("config.json")
    if network.WLAN(network.STA_IF).isconnected():
        haPayloadGenerator = PayloadGenerator("UUID", myconfig)
        print(myconfig.wifi_config)
        print(myconfig.mqtt_config)
        print(haPayloadGenerator.getDiscoveryPayloads())
        haMqttClient = MqttClient(
            myconfig.output_config,
            haPayloadGenerator.getDiscoveryPayloads(),
            haPayloadGenerator.getDiscoveryTopics(),
            haPayloadGenerator.getSetTopicMap(),
            MQTTClient(
                client_id=haPayloadGenerator.getUUID(),
                server=myconfig.mqtt_config.host,
                user=myconfig.mqtt_config.user,
                password=myconfig.mqtt_config.password),
            machine)
        haMqttClient.mqttInitialise(True)
    else:
        print("Couldn't connect to any of the specified SSIDs, exiting")
    try:
        # while 1 and network.WLAN(network.STA_IF).isconnected():
        while 1:
            haMqttClient.mqttClient.wait_msg()
    finally:
        haMqttClient.mqttStatus(False)
        haMqttClient.defaultOutputsToOff()
        haMqttClient.mqttClient.disconnect()
        led.off()

main()
