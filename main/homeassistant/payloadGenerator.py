from umqtt.simple import MQTTClient
from .discoveryPayload import HomeAssistantDiscoveryBuilder
from .disoveryDevice import DiscoveryDevice
from main.configparsing.output import Output
from main.configparsing.configparser import ConfigParser
from main.configparsing.homeassistantdiscoveryconfig import HomeAssistantDiscoveryConfig
import json, machine

class PayloadGenerator:
    topic_prefix: str
    outputs: list[Output]
    ha_discovery: HomeAssistantDiscoveryConfig
    location: str
    UUID: str
    
    def __init__(self, UUID: str, parsedConfig: ConfigParser):
        if UUID:
            self.UUID = UUID
        else:
            self.UUID = "testUUID"
        self.topic_prefix = parsedConfig.mqtt_config.topic_prefix
        self.outputs = parsedConfig.output_config
        self.ha_discovery = parsedConfig.mqtt_config.ha_discovery
        self.location = parsedConfig.mqtt_config.location
        self.haDiscoveryPayloads = []
        self.haDiscoveryTopics = None
        self.setTopicMap = {}
        if self.ha_discovery.enabled != None:
            self.initHaDiscovery()

    def initHaDiscovery(self) -> None:
        self.createDiscoveryPayloads()
        self.createDiscoveryTopics()

    def createDiscoveryTopics(self) -> None:
        self.haDiscoveryTopics = [self.ha_discovery.discovery_topic_prefix + self.UUID+"/"+output.name+"/config" for output in self.outputs]

    def createDiscoveryPayloads(self) -> None:
        for output in self.outputs:
            state_topic = self.location+"/output/"+output.name
            command_topic = self.location+"/output/"+output.name+"/set"
            outputDiscoveryPayload =  HomeAssistantDiscoveryBuilder()\
            .set_name(output.name)\
            .set_availability_topic(self.topic_prefix + "/status")\
            .set_device(
                DiscoveryDevice(
                    "Home Assistant MQTT Client",
                    "v0",
                    ["Home Assistant MQTT Client", "Home Assistant MQTT Client-"+self.UUID],
                    "Home Assistant MQTT Client")
                )\
            .set_unique_id(self.UUID)\
            .set_state_topic(state_topic)\
            .set_command_topic(command_topic)\
            .set_payload_on(output.on_payload)\
            .set_payload_off(output.off_payload)\
            .build().return_map()
            self.haDiscoveryPayloads.append(outputDiscoveryPayload)
            self.setTopicMap[command_topic] = {"state_topic": state_topic, "output": output}
           
    def getUUID(self) -> str:
        return self.UUID
    
    def getDiscoveryPayloads(self) -> list[map]:
        return self.haDiscoveryPayloads
    
    def getDiscoveryTopics(self) -> list[str]:
        return self.haDiscoveryTopics
    
    def getSetTopicMap(self) -> map[map]:
        return self.setTopicMap
    
