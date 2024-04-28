from main.configparsing.configparser import ConfigParser
from main.Pi2040Home import Pi2040Home


def main():
    Pi2040Home(ConfigParser().load("config.json")).connect_wlan().start_connection()

main()
