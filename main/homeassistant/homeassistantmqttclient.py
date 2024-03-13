from umqtt.simple import MQTTClient
from .homeassistantdiscovery import HomeAssistantDiscoveryBuilder
from .homeassistantdiscoverydevice import HomeAssistantDiscoveryDevice
from main.configparsing.output import Output
from main.configparsing.configparser import ConfigParser
from main.configparsing.homeassistantdiscoveryconfig import HomeAssistantDiscoveryConfig
import json, machine

class HomeAssistantMqttClient:
    topic_prefix: str
    outputs: list[Output]
    ha_discovery: HomeAssistantDiscoveryConfig
    location: str
    UUID: str
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
        self.haDiscoveryPayloads = []
        self.haDiscoveryTopics = None
        self.setTopicMap = {}
        self.mqtt_client = MQTTClient(
            client_id=self.UUID,
            server=parsedConfig.mqtt_config.host,
            user=parsedConfig.mqtt_config.user,
            password=parsedConfig.mqtt_config.password)
        if self.ha_discovery.enabled != None:
            self.initHaDiscovery()

    def initHaDiscoveryTopics(self) -> None:
        self.haDiscoveryTopics = [self.ha_discovery.discovery_topic_prefix + self.UUID+"/"+output.name+"/config" for output in self.outputs]

    def initHaDiscoveryPayloads(self) -> None:
        for output in self.outputs:
            state_topic = self.location+"/output/"+output.name
            command_topic = self.location+"/output/"+output.name+"/set"
            outputDiscoveryPayload =  HomeAssistantDiscoveryBuilder()\
            .set_name(output.name)\
            .set_availability_topic(self.topic_prefix + "/status")\
            .set_device(
                HomeAssistantDiscoveryDevice(
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
           

    def defaultOutputsToOff(self) -> None:
        for output in self.outputs:
            machine.Pin(output.pin, machine.Pin.OUT).off()
        for payload in self.haDiscoveryPayloads:
            self.mqtt_client.publish(payload["state_topic"], payload["payload_off"])
    
    def initHaDiscovery(self) -> None:
        self.initHaDiscoveryPayloads()
        self.initHaDiscoveryTopics()
    
    def mqttStatus(self, isAvailable) -> None:
        for haDiscovery in self.haDiscoveryPayloads:
            if isAvailable:
                self.publish(
                    haDiscovery["availability_topic"], haDiscovery["payload_available"])
                continue
            self.publish(haDiscovery["availability_topic"], haDiscovery["payload_not_available"])

    def mqttHADiscoveryPost(self) -> None:
        for haDiscovery, haDiscoveryTopic in zip(self.haDiscoveryPayloads, self.haDiscoveryTopics):
            self.publish(haDiscoveryTopic, json.dumps(haDiscovery))
            self.mqtt_client.subscribe(haDiscovery["command_topic"])

    def action(self, topic, msg) -> None:
        topicString = topic.decode()
        msgString = msg.decode()
        print("Topic: " + topicString + "; Message: " + msgString)
        if self.setTopicMap.get(topicString) is None:
            return
        topicOutput = self.setTopicMap.get(topicString).get("output")
        topicStateTopic = self.setTopicMap.get(topicString).get("state_topic")
        self.mqtt_client.publish(topicStateTopic, msgString)
        if msgString == topicOutput.on_payload:
            machine.Pin(topicOutput.pin, machine.Pin.OUT).on()
            return
        if msgString == topicOutput.off_payload:
            machine.Pin(topicOutput.pin, machine.Pin.OUT).off()
            return
        print("did not match either on or off payload - error")
            

    def mqttInitialise(self, isAvailable) -> None:
        self.mqtt_client.set_callback(self.action)
        self.mqtt_client.connect()
        self.mqttHADiscoveryPost()
        self.defaultOutputsToOff()
        self.mqttStatus(isAvailable)
        
    
    def publish(self, topic: str, payload: any) -> None:
        self.mqtt_client.publish(topic, payload)
