class HomeAssistantDiscoveryConfig:
    enabled: str
    discovery_topic_prefix: str
    
    def __init__(self, enabled:str, discovery_topic_prefix: str):
        self.enabled = enabled
        self.discovery_topic_prefix = discovery_topic_prefix
