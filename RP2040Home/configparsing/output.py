from RP2040Home.configparsing.inputsanitisation import InputSanitisation


class Output:
    output_type: str
    name: str
    pin: int
    on_payload: str
    off_payload: str

    def __init__(self, output_type: str, name: str, pin: int, on_payload: str, off_payload: str):
        self.output_type = InputSanitisation().clean_string(output_type)
        self.name = InputSanitisation().clean_string(name)
        self.pin = pin
        self.on_payload = InputSanitisation().clean_string(on_payload)
        self.off_payload = InputSanitisation().clean_string(off_payload)

    def __eq__(self, other):
        if not isinstance(other, Output):
            return False
        return (
            self.output_type == other.output_type and
            self.name == other.name and
            self.pin == other.pin and
            self.on_payload == other.on_payload and
            self.off_payload == other.off_payload
        )
