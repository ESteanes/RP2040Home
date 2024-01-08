class MqttConfig:
    keys = ['host', 'port', 'user', 'passwod', 'topic_prefix', 'ha_discovery']
    host: str
    port: int
    user: str
    password: str
    topic_prefix: str
    ha_discovery: list[dict]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
