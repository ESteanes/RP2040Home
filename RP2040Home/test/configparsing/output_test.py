import unittest
from RP2040Home.configparsing.output import Output


class TestOutput(unittest.TestCase):

    def test_output_equality(self):
        output1 = Output('switch', 'myOutput', 17, 'ON', 'OFF')
        output2 = Output('switch', 'myOutput', 17, 'ON', 'OFF')
        output3 = Output('switch', 'anotherOutput', 18, 'ON', 'OFF')

        self.assertEqual(output1, output2)  # Should be equal
        self.assertNotEqual(output1, output3)  # Should not be equal

    def test_list_of_outputs_equality(self):
        list1 = [Output('switch', 'myOutput', 17, 'ON', 'OFF')]
        list2 = [Output('switch', 'myOutput', 17, 'ON', 'OFF')]

        self.assertEqual(list1, list2)  # Should be equal


if __name__ == '__main__':
    unittest.main()
