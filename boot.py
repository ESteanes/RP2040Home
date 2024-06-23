# This file is executed on every boot (including wake-boot from deepsleep)

import gc
import time
import network
from RP2040Home.configparsing.configparser import ConfigParser

gc.collect()


def connect():
    myconfig = ConfigParser()
    myconfig.load("config.json")
    sta_if = network.WLAN(network.STA_IF)
    networkConnectTimer = 0
    if not sta_if.isconnected():
        print('Connecting to network...')
        for wifiConnection in myconfig.wifi_config:
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


connect()
