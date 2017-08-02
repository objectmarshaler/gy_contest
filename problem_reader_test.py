import unittest
from problem_reader import ProblemReader

class ProblemReaderTest(unittest.TestCase):
	def test_read(self):
		reader = ProblemReader()
		reader.read("data\\")
		self.assertTrue(len(reader.link_info)>0)
		self.assertTrue(len(reader.link_top)>0)


if __name__ == '__main__':
    unittest.main()



