from .mqttconfig import MqttConfig
from .output import Output
from .wificonfig import WifiConfig
import json


class ConfigParser:
    wifi_config: list[WifiConfig]
    mqtt_config: MqttConfig
    output_config: list[Output]
    allowed_pins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 26, 27, 28]

    def load(self, path_to_file):
        with open(path_to_file, "r") as stream:
            config = json.loads(stream.read())
            self.parse_config(config)
            self.validate_config(config, self.allowed_pins, self.output_config)
        return self

    def load_from_object(self, config):
        self.parse_config(config)
        self.validate_config(config, self.allowed_pins, self.output_config)
        return self

    def parse_config(self, config: any):
        self.wifi_config = [WifiConfig(wifiConfig["ssid"], wifiConfig["password"]) for wifiConfig in config['pi']]
        self.mqtt_config = MqttConfig(**config['mqtt'])
        if config['digital_outputs']:
            self.output_config = [
                Output(
                    x["output_type"],
                    x['name'],
                    x['pin'],
                    x['on_payload'],
                    x['off_payload']
                ) for x in config['digital_outputs'] if x['pin'] in self.allowed_pins]

    def validate_config(self, config: any, allowed_pins: list[str], output_config: list[Output]):
        for x in config['digital_outputs']:
            if x['pin'] not in allowed_pins:
                raise AttributeError(
                    "Output on " + str(x['pin']) +
                    " is not allowed, the only allowed GPIO pins are: "
                    + ",".join(map(str, allowed_pins))
                    )
        if len(output_config) == 0 and len(config['digital_outputs']) == 0:
            print("No digital outputs")
            raise ValueError("No output values are defined in config")
        if len(output_config) != len(config['digital_outputs']):
            raise AttributeError(
                "One or more outputs has been misconfigured, the only allowed GPIO pins are: "
                + ",".join(map(str, allowed_pins))
                )
        try:
            print(config)
        except json.JSONDecodeError as exc:
            print(exc)
            raise RuntimeError("Unable to print the json config.")
