import unittest

from mock import MagicMock, patch

from bloomon.utils import BouquetService, BouquetData, ExtractedInput


class BouquetServiceTest(unittest.TestCase):

    def test__happy_flow_apply(self):
        bouquet_data_mock = MagicMock(specset=BouquetData)
        bouquet_data_mock.name = 'Cherry Blossoms'
        bouquet_data_mock.flowers = {'x': 1, "y": 3}
        bouquet_data_mock.specifications = {'x': 1, "y": 3}

        apply = BouquetService(bouquet_data_mock).apply()
        self.assertTrue(bouquet_data_mock.name in apply)


class ExtractedInputTest(unittest.TestCase):
    def setUp(self) -> None:
        self.design = 'AL8d10r5t30\n'
        self.flowers = 'rL\ndL\n'

    def test_get_design(self):
        extract = ExtractedInput(self.design, self.flowers).get_design()
        self.assertTrue('AL8d10r5t30' in extract)

    def test_get_flower(self):
        extract = ExtractedInput(self.design, self.flowers).get_flowers()
        self.assertTrue('rL' in extract)
        self.assertTrue('dL' in extract)


if __name__ == '__main__':
    unittest.main()