from RP2040Home.configparsing.inputsanitisation import InputSanitisation


class HomeAssistantDiscoveryConfig:
    enabled: str
    node_id: str

    def __init__(self, enabled: str, node_id: str):
        self.enabled = InputSanitisation().clean_string(enabled)
        self.node_id = InputSanitisation().clean_string(node_id)

    def __eq__(self, other):
        if not isinstance(other, HomeAssistantDiscoveryConfig):
            return False
        return self.__dict__ == other.__dict__
