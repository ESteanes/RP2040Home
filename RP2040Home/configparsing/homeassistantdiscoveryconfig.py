from RP2040Home.configparsing.configparser import ConfigParser

class HomeAssistantDiscoveryConfig:
    enabled: str
    node_id: str
    
    def __init__(self, enabled:str, node_id: str):
        self.enabled = ConfigParser.clean_string(enabled)
        self.node_id = ConfigParser.clean_string(node_id)
