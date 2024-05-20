from RP2040Home.configparsing.configparser import ConfigParser

class Output:
    output_type: str
    name: str
    pin: int
    on_payload: str
    off_payload: str

    def __init__(self, output_type:str, name: str, pin: int, on_payload: str, off_payload: str):
        self.output_type = ConfigParser.clean_string(output_type)
        self.name = ConfigParser.clean_string(name)
        self.pin = ConfigParser.clean_string(pin)
        self.on_payload = ConfigParser.clean_string(on_payload)
        self.off_payload = ConfigParser.clean_string(off_payload)
