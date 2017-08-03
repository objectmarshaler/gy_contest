import csv
import sys
from datetime import datetime

class ProblemReader(object):
    """
        Convert problem into samples which can be used to train decision trees.
    """

    def __init__(self):
        self.link_info = {}
        self.link_top = {}
        #self.link_traveltime_training_data = []

    def read(self, dir):
        """read training data.
        """
        link_info_rows = self._load_csv(dir + "gy_contest_link_info.txt")
        for row in link_info_rows:
            self.link_info[row["link_ID"]] = [
                row["length"], row["width"], row["link_class"]]
        # in links and out links.
        link_top_rows = self._load_csv(dir + "gy_contest_link_top.txt")
        for row in link_top_rows:
            self.link_top[row["link_ID"]] = [
                row["in_links"].split('#'), row["out_links"].split('#')]

        return

    def preprocess_training_data(self, file_name):
        link_traveltime_training_data = self._load_csv(
            file_name
        )
        samples = []
        link_traveltime_training_data.sort(key=lambda row: row['date'])
        date = link_traveltime_training_data[0]["date"]
        for row in link_traveltime_training_data:
            if(row["date"] != date):
                self._write_csv("data\\training_data\\" + date + ".csv", samples)
                del samples[:]
                date = row["date"]
            else:
                sample = {}
                sample["link_ID"] = row["link_ID"]
                sample["length"] = self.link_info[sample["link_ID"]][0]
                sample["width"] = self.link_info[sample["link_ID"]][1]
                sample["link_class"] = self.link_info[sample["link_ID"]][2]
                
                time = datetime.strptime(row["time_interval"].split(',')[0][1:],"%Y-%m-%d %H:%M:%S")
                sample["weekday"] = time.weekday()
                sample["date"] = time.month + (time.day/31)
                sample["time"] = time.hour + (time.minute/60)
                sample["travel_time"] = row["travel_time"]
                samples.append(sample)
        return

    def _load_csv(self, filename):
        rows = []
        with open(filename, 'rt') as f:
            reader = csv.DictReader(f, delimiter=';')
            try:
                for row in reader:
                    rows.append(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' %
                         (filename, reader.line_num, e))
        return rows

    def _write_csv(self, filename, rows):
        rows.sort(key = lambda row:row["time"])
        with open(filename, 'w') as csvfile:
            fieldnames = ['link_ID', 'length', 'width', 'link_class','weekday','date','time','travel_time']
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
