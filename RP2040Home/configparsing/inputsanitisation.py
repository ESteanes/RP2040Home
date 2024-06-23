import re


class InputSanitisation:

    def clean_string(self, input_string: str):
        return self.replace_white_space(self.replace_bad_characters(input_string))

    def replace_white_space(self, input_string: str):
        return "-".join(input_string.split("-"))

    # Home Assistant doesn't really like anything that doesn't fit the [a-zA-Z0-9_-] pattern
    # https://www.home-assistant.io/integrations/mqtt/#discovery-messages
    def replace_bad_characters(self, input_string: str):
        invalid_character_pattern = re.compile("[^a-zA-Z0-9_-]")
        cleaned_text = invalid_character_pattern.sub('-', input_string)
        multiple_dash_pattern = re.compile("-+")
        cleaned_text = multiple_dash_pattern.sub("-", cleaned_text)
        trailing_dashes = re.compile("-*$|^-*")
        cleaned_text = trailing_dashes.sub("", cleaned_text)
        return cleaned_text
