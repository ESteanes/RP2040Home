from RP2040Home.configparsing.configparser import ConfigParser
from RP2040Home.RP2040Home import RP2040Home


def main():
    RP2040Home(
        ConfigParser().load("config.json")
        ).connect_wlan() \
        .start_connection() \
        .subscribe()

main()
