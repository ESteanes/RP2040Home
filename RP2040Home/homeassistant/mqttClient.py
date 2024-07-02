import json
import machine
from umqtt.simple import MQTTClient
from RP2040Home.configparsing.output import Output
from RP2040Home.homeassistant.discoveryPayload import DiscoveryPayload


class MqttClient:
    def __init__(
            self,
            outputs: list[Output],
            haDiscoveryPayloads: list[DiscoveryPayload],
            haDiscoveryTopics: list[str],
            setTopicMap: map[map],
            mqttClient: MQTTClient,
            ioInteractor: machine) -> None:
        self.outputs = outputs
        self.haDiscoveryPayloads = haDiscoveryPayloads
        self.haDiscoveryTopics = haDiscoveryTopics
        self.setTopicMap = setTopicMap
        self.ioInteractor = ioInteractor
        self.mqttClient = mqttClient

    def defaultOutputsToOff(self) -> None:
        for output in self.outputs:
            self.ioInteractor.Pin(output.pin, self.ioInteractor.Pin.OUT).off()
        for haDiscoveryPayload in self.haDiscoveryPayloads:
            self.publish(haDiscoveryPayload.get_state_topic(), haDiscoveryPayload.get_payload_off())

    def mqttStatus(self, isAvailable) -> None:
        for haDiscoveryPayload in self.haDiscoveryPayloads:
            if isAvailable:
                self.publish(haDiscoveryPayload.get_availability_topic(), haDiscoveryPayload.get_payload_available())
                continue
            self.publish(haDiscoveryPayload.get_availability_topic(), haDiscoveryPayload.get_payload_not_available())

    def mqttHADiscoveryPost(self) -> None:
        for discoveryPayload, haDiscoveryTopic in zip(self.haDiscoveryPayloads, self.haDiscoveryTopics):
            disoveryPayloadString = json.dumps(discoveryPayload.return_map())
            self.publish(haDiscoveryTopic, disoveryPayloadString)
            print("publishing to:" + haDiscoveryTopic)
            print("discovery payload:" + disoveryPayloadString)
            self.mqttClient.subscribe(discoveryPayload.get_command_topic())
            print("subscribing to:" + discoveryPayload.get_command_topic())

    def action(self, topic, msg) -> None:
        topicString = topic.decode()
        msgString = msg.decode()
        print("Topic: " + topicString + "; Message: " + msgString)
        if self.setTopicMap.get(topicString) is None:
            return
        topicOutput = self.setTopicMap.get(topicString).get("output")
        topicStateTopic = self.setTopicMap.get(topicString).get("state_topic")
        self.publish(topicStateTopic, msgString)
        if msgString == topicOutput.on_payload:
            self.ioInteractor.Pin(topicOutput.pin, self.ioInteractor.Pin.OUT).on()
            return
        if msgString == topicOutput.off_payload:
            self.ioInteractor.Pin(topicOutput.pin, self.ioInteractor.Pin.OUT).off()
            return
        print("did not match either on or off payload - error")

    def mqttInitialise(self, isAvailable) -> None:
        self.mqttClient.set_callback(self.action)
        self.mqttClient.connect()
        self.mqttHADiscoveryPost()
        self.defaultOutputsToOff()
        self.mqttStatus(isAvailable)

    def publish(self, topic: str, payload: any) -> None:
        self.mqttClient.publish(topic, payload)
