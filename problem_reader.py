import csv
import sys
from datetime import datetime, timedelta

class ProblemReader(object):
    """
        Convert problem into samples which can be used to train decision trees.
    """

    def __init__(self):
        self.link_info = {}
        self.link_top = {}
        #self.link_traveltime_training_data = []

    def read_link_info(self, dir):
        """read training data.
        """
        link_info_rows = self._load_csv_by_dict_reader(dir + "gy_contest_link_info.txt")
        for row in link_info_rows:
            self.link_info[row["link_ID"]] = [
                row["length"], row["width"], row["link_class"]]
        # in links and out links.
        link_top_rows = self._load_csv_by_dict_reader(dir + "gy_contest_link_top.txt")
        for row in link_top_rows:
            self.link_top[row["link_ID"]] = [
                row["in_links"].split('#'), row["out_links"].split('#')]

        return

    def preprocess_training_data(self, file_name):
        link_traveltime_training_data = self._load_csv_by_dict_reader(
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

    def read_variables(self, dir, start_date_str, end_date_str = None, start_hour = None,end_hour = None):
        start_date = datetime.strptime(start_date_str,"%Y-%m-%d")
        end_date = start_date
        if(end_date_str != None):
            end_date = datetime.strptime(end_date_str,"%Y-%m-%d")
        variables = []
        current_date = start_date
        while(current_date <= end_date):
            variables.extend(self._load_csv_by_reader(dir+current_date.strftime("%Y-%m-%d"+".csv")))
            current_date = current_date + timedelta(days=1)
        
        for i in range(len(variables)):
            variables[i] = [self._num(x) for x in  variables[i]]
        
        return variables

    def _load_csv_by_dict_reader(self, filename):
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

    def _load_csv_by_reader(self, filename):
        rows = []
        with open(filename, 'rt') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)
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
    
    def _num(self,s):
        try:
            return int(s)
        except ValueError:
            return float(s)
