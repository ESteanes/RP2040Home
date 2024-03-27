
class Output:
    name: str
    pin: int
    on_payload: str
    off_payload: str

    def __init__(self, name: str, pin: int, on_payload: str, off_payload: str):
        self.name = name
        self.pin = pin
        self.on_payload = on_payload
        self.off_payload = off_payload
