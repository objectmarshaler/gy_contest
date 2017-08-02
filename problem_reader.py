import csv
import sys


class ProblemReader(object):
    """
    """
    link_info = []
    link_top = []

    def read(self, dir):
		"""read training data.
		"""
		self.link_info = self._load_csv(dir + "gy_contest_link_info.txt")
		self.link_top = self._load_csv(dir + "gy_contest_link_top.txt")
		return

    def _load_csv(self, filename):
        rows = []
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    rows.append(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' %
                         (filename, reader.line_num, e))
		
		return rows