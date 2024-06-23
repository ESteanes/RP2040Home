from RP2040Home.configparsing.homeassistantdiscoveryconfig import HomeAssistantDiscoveryConfig
from RP2040Home.configparsing.inputsanitisation import InputSanitisation


class MqttConfig:
    keys = [
        'host',
        'port',
        'user',
        'password',
        'topic_prefix',
        'location',
        'ha_discovery'
        ]
    host: str
    port: int
    user: str
    password: str
    topic_prefix: str
    location: str
    ha_discovery: HomeAssistantDiscoveryConfig

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'ha_discovery':
                self.ha_discovery = HomeAssistantDiscoveryConfig(**value)
                continue
            if key == 'location':
                setattr(self, key, InputSanitisation().clean_string(value))
                continue
            # We don't want to clean anything that isn't going into Home Assistant related payloads
            setattr(self, key, value)
        for key in self.keys:
            if key not in kwargs:
                raise AttributeError("The attribute \'"+key+"\' is missing - please check your configuration file")

    def __eq__(self, other):
        if not isinstance(other, MqttConfig):
            return False
        return self.__dict__ == other.__dict__
