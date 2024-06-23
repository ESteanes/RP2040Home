from RP2040Home.configparsing.configparser import ConfigParser
from RP2040Home.homeassistant.payloadGenerator import PayloadGenerator
from RP2040Home.homeassistant.mqttClient import MqttClient

import time
import network
import machine
from machine import Timer
from umqtt.simple import MQTTClient


class RP2040Home:
    seconds_to_ms = 1000
    minutes_to_seconds = 60
    config: ConfigParser
    haMqttClient: MqttClient

    def __init__(self, config: ConfigParser):
        self.config = config
        if config is None:
            raise ValueError("Config value must be set")
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led.on()

    def connect_wlan(self):
        sta_if = network.WLAN(network.STA_IF)
        networkConnectTimer = 0
        if not sta_if.isconnected():
            print('Connecting to network...')
            for wifiConnection in self.config.wifi_config:
                print("Attempting to join ssid" + wifiConnection.ssid)
                sta_if.active(True)
                sta_if.connect(wifiConnection.ssid, wifiConnection.password)
                while not sta_if.isconnected() and networkConnectTimer < 30:
                    pass
                    time.sleep(1)
                    networkConnectTimer += 1
                if sta_if.isconnected():
                    break
                networkConnectTimer = 0
        print('Network config:', sta_if.ifconfig())
        return self

    def start_connection(self):
        if not network.WLAN(network.STA_IF).isconnected():
            print("Couldn't connect to any of the specified SSIDs, exiting")
            self.led.off()
            return

        haPayloadGenerator = PayloadGenerator(self.config)
        print(self.config.wifi_config)
        print(self.config.mqtt_config)
        print(haPayloadGenerator.getDiscoveryPayloads())
        self.haMqttClient = MqttClient(
            self.config.output_config,
            haPayloadGenerator.getDiscoveryPayloads(),
            haPayloadGenerator.getDiscoveryTopics(),
            haPayloadGenerator.getSetTopicMap(),
            MQTTClient(
                client_id=haPayloadGenerator.getUUID(),
                server=self.config.mqtt_config.host,
                user=self.config.mqtt_config.user,
                password=self.config.mqtt_config.password),
            machine)
        self.haMqttClient.mqttInitialise(True)
        return self

    def subscribe(self):
        def my_dicovery_callback(t):
            self.haMqttClient.mqttHADiscoveryPost()

        def my_wlan_connect_callback(t):
            self.connect_wlan()

        ten_minutes_as_ms = 10*self.minutes_to_seconds*self.seconds_to_ms
        timer_ha_discover = Timer(
            period=ten_minutes_as_ms,
            mode=Timer.PERIODIC,
            callback=my_dicovery_callback)
        timer_wlan_connect = Timer(
            period=ten_minutes_as_ms,
            mode=Timer.PERIODIC,
            callback=my_wlan_connect_callback)

        try:
            while 1:
                self.haMqttClient.mqttClient.wait_msg()

        finally:
            self.haMqttClient.mqttStatus(False)
            self.haMqttClient.defaultOutputsToOff()
            self.haMqttClient.mqttClient.disconnect()
            timer_ha_discover.deinit()
            timer_wlan_connect.deinit()
            self.led.off()
