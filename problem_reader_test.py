import unittest
from problem_reader import ProblemReader


class ProblemReaderTest(unittest.TestCase):
    def test_read(self):
        reader = ProblemReader()
        reader.read("data\\")
        self.assertTrue(len(reader.link_info) > 0)
        self.assertTrue(len(reader.link_top) > 0)
        self.assertTrue(reader.link_info['4377906289869500514'][0] == '57')
        self.assertTrue(
            reader.link_top['4377906284422600514'][0][0] == '3377906289434510514')

    def test_preprocess_training_data(self):
        reader = ProblemReader()
        reader.read("data\\")
        reader.preprocess_training_data("data\\test.txt")


if __name__ == '__main__':
    unittest.main()
