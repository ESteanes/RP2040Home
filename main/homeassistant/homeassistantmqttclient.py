from umqtt.simple import MQTTClient
from homeassistant.homeassistantdiscovery import HomeAssistantDiscoveryBuilder
from homeassistant.homeassistantdiscoverydevice import HomeAssistantDiscoveryDevice
from configparsing.output import Output
from configparsing.configparser import ConfigParser
from configparsing.homeassistantdiscoveryconfig import HomeAssistantDiscoveryConfig


class HomeAssistantMqttClient:
    topic_prefix: str
    outputs: list[Output]
    ha_discovery: HomeAssistantDiscoveryConfig
    location: str
    UUID: str
    haDiscoveryPayloads = list[map]
    mqtt_client: MQTTClient
    
    def __init__(self, UUID: str, parsedConfig: ConfigParser):
        if UUID:
            self.UUID = UUID
        else:
            self.UUID = "testUUID"
        self.topic_prefix = parsedConfig.mqtt_config.topic_prefix
        self.outputs = parsedConfig.output_config
        self.ha_discovery = parsedConfig.mqtt_config.ha_discovery
        self.location = parsedConfig.mqtt_config.location
        self.haDiscoveryPayloads = None
        self.haDiscoveryTopics = None
        self.mqtt_client = MQTTClient(
            client_id=self.UUID,
            server=parsedConfig.mqtt_config.host,
            user=parsedConfig.mqtt_config.user,
            password=parsedConfig.mqtt_config.password)
        if self.ha_discovery.enabled != None:
            self.initHaDiscovery()

    def initHaDiscoveryTopics(self):
        self.haDiscoveryTopics = [self.ha_discovery.discovery_topic_prefix + self.UUID+"/"+output.name+"/config" for output in self.outputs]

    def initHaDiscoveryPayloads(self):
        self.haDiscoveryPayloads = [
            HomeAssistantDiscoveryBuilder()
            .name(output.name)
            .availability_topic(self.topic_prefix + "/status")
            .device(
                HomeAssistantDiscoveryDevice(
                    "Home Assistant MQTT Client",
                    "v0",
                    ["Home Assistant MQTT Client", "Home Assistant MQTT Client-"+self.UUID],
                    "Home Assistant MQTT Client")
                )
            .unique_id(self.UUID)
            .state_topic(self.location+"/output/"+output.name)
            .command_topic(self.location+"/output/"+output.name+"/set")
            .payload_on(output.on_payload)
            .payload_off(output.off_payload)
            .build().return_map() for output in self.outputs]

    def initHaDiscovery(self):
        self.initHaDiscoveryPayloads()
        self.initHaDiscoveryTopics()
    
    def mqttStatus(self, isAvailable):
        for haDiscovery in self.haDiscoveryPayloads:
            if isAvailable:
                self.publish(
                    haDiscovery["availability_topic"], haDiscovery["payload_available"])
                continue
            self.publish(haDiscovery["availability_topic"], haDiscovery["payload_not_available"])

    def mqttHADiscoveryPost(self):
        for haDiscovery in self.haDiscoveryPayloads:
            self.publish(haDiscovery["availability_topic"],haDiscovery)

    def mqttInitialise(self, isAvailable):
        self.mqttStatus(isAvailable)
        self.mqttInitialise()
    
    def publish(self, topic: str, payload: any) -> None:
        self.mqtt_client.publish(topic, payload)
