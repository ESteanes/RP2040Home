
class WifiConfig:
    ssid: str
    password: str

    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password

    def __eq__(self, other):
        if not isinstance(other, WifiConfig):
            return False
        return self.__dict__ == other.__dict__
