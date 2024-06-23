import unittest
from RP2040Home.configparsing.inputsanitisation import InputSanitisation


class InputSanitisation_Test(unittest.TestCase):

    def setUp(self):
        self.input_sanitiser = InputSanitisation()

    def test_clean_string(self):
        dirty_string = "This is a string with spaces and forbidden characters~!@#"
        expected_string = "This-is-a-string-with-spaces-and-forbidden-characters"
        self.assertEqual(expected_string, self.input_sanitiser.clean_string(dirty_string))

    def test_clean_string_multiple_spaces(self):
        dirty_string = "This is a string with multiple      spaces and forbidden characters~!@#"
        expected_string = "This-is-a-string-with-multiple-spaces-and-forbidden-characters"
        self.assertEqual(expected_string, self.input_sanitiser.clean_string(dirty_string))

    def test_clean_string_leading_characters(self):
        dirty_string = "!@#%----This is a string with multiple      spaces and forbidden characters~!@#"
        expected_string = "This-is-a-string-with-multiple-spaces-and-forbidden-characters"
        self.assertEqual(expected_string, self.input_sanitiser.clean_string(dirty_string))


if __name__ == '__main__':
    unittest.main()
