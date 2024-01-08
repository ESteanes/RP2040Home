from umqtt.simple import MQTTClient
from .HomeAssistantDiscovery import HomeAssistantDiscoveryBuilder
from .HomeAssistantDiscoveryDevice import HomeAssistantDiscoveryDevice
from ..config_parsing.Output import Output



class HomeAssistantMqttClient:
    def __init__(self, ha_discovery: bool, topic_prefix: str, UUID: str, outputs: list[Output], mqtt_server_host: str, mqtt_username: str, mqtt_password: str):
        if UUID:
            self.UUID = UUID
        else:
            self.UUID = "testUUID"
        self.topic_prefix = topic_prefix
        self.outputs = outputs
        self.ha_discovery = ha_discovery
        self.location = "test"
        self.haDiscoveryPayloads = None
        self.mqtt_client = MQTTClient(client_id=self.UUID,server=mqtt_server_host, user=mqtt_username, password=mqtt_password)
        if ha_discovery:
            self.initHaDiscovery()
# returns a list of HA Discovery dictionaries

    def initHaDiscovery(self):
        self.haDiscoveryPayloads = [
        
        HomeAssistantDiscoveryBuilder()
        .name(output.name)
        .availability_topic(self.topic_prefix + "/status")
        .device(HomeAssistantDiscoveryDevice("Ellington Steanes", "Pico Watering Device", ["ES-Watering", "ES-Watering-"+self.UUID],"Pico MQTT"))
        .unique_id("ES-Watering-UUID-"+self.UUID)
        .state_topic(self.location+"/output/"+output.name)
        .command_topic(self.location+"/output/"+output.name+"/set")
        .payload_on(output.on_payload)
        .payload_off(output.off_payload)
        .build().return_payload() for output in self.outputs]

        self.haDiscoveryTopics = ["homeassistant/switch/ES-Watering-" +
                                  self.UUID+"/"+output.name+"/config" for output in self.outputs]

    def mqttStatus(self, isAvailable):
        for haDiscovery in self.haDiscoveryPayloads:
            if isAvailable:
                self.publish(
                    haDiscovery["availability_topic"], haDiscovery["payload_available"])
            else:
                self.publish(
                    haDiscovery["availability_topic"], haDiscovery["payload_not_available"])

    def mqttHADiscoveryPost(self):
        for haDiscovery in self.haDiscoveryPayloads:
            self.publish(haDiscovery["availability_topic"],haDiscovery)

    def publish(self, topic: str, payload) -> None:
        self.mqtt_client.publish(topic, payload)
