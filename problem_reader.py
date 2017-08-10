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
        link_info_rows = self._load_csv_by_dict_reader(
            dir + "gy_contest_link_info.txt")
        for row in link_info_rows:
            self.link_info[row["link_ID"]] = [
                row["length"], row["width"], row["link_class"]]
        # in links and out links.
        link_top_rows = self._load_csv_by_dict_reader(
            dir + "gy_contest_link_top.txt")
        for row in link_top_rows:
            related_links = []
            in_links = row["in_links"].split('#')
            out_links = row["out_links"].split('#')
            if(in_links[0]):
                related_links.extend(in_links)
            if(out_links[0]):
                related_links.extend(out_links)
            self.link_top[row["link_ID"]] = related_links

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
                self._write_csv("data\\training_data\\" +
                                date + ".csv", samples)
                del samples[:]
                date = row["date"]

            sample = {}
            sample["link_ID"] = row["link_ID"]
            sample["length"] = self.link_info[sample["link_ID"]][0]
            sample["width"] = self.link_info[sample["link_ID"]][1]
            sample["link_class"] = self.link_info[sample["link_ID"]][2]

            time = datetime.strptime(row["time_interval"].split(',')[
                                     0][1:], "%Y-%m-%d %H:%M:%S")
            sample["weekday"] = time.weekday()
            sample["date"] = time.month + (time.day / 31)
            sample["time"] = time.hour + (time.minute / 60)
            sample["travel_time"] = row["travel_time"]
            samples.append(sample)

        self._write_csv("data\\training_data\\" +
                        date + ".csv", samples)
        return

    def read_variables(self, dir, start_date_str, end_date_str=None, start_hour=None, end_hour=None):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = start_date
        if(end_date_str != None):
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        variables = []
        current_date = start_date
        while(current_date <= end_date):
            variables.extend(self._load_csv_by_reader(
                dir + current_date.strftime("%Y-%m-%d" + ".csv")))
            current_date = current_date + timedelta(days=1)

        for i in range(len(variables)):
            variables[i] = [self._num(x) for x in variables[i]]

        variables.sort(key=lambda x: (x[-3], x[-2]))
        return variables

    def group_variables_by_link(self, variables):
        links_map = set(map(lambda x: x[0], variables))
        variables_group_by_links = {x:
                                    [variable for variable in variables if variable[0] == x] for x in links_map}
        return variables_group_by_links

    def find_neighboring_routes(self, variables_group_by_link, link, date, time):
        neighboring_links = []
        in_link = self._num(self.link_top[str(link)][0])
        out_link = self._num(self.link_top[str(link)][-1])
        if(in_link in variables_group_by_link):
            recent_variable = self.find_most_recent_route(
                variables_group_by_link[in_link], date, time)
            if(recent_variable):
                neighboring_links.append(recent_variable)
        if (out_link in variables_group_by_link):
            recent_variable = self.find_most_recent_route(
                variables_group_by_link[out_link], date, time)
            if(recent_variable):
                neighboring_links.append(recent_variable)

        return neighboring_links

    def find_most_recent_route(self, variables, date, time):
        recent_route = None
        timespan = float('inf')
        variables_filter_by_date = [
            variable for variable in variables if variable[-3] == date]
        for variable in variables_filter_by_date:
            if(variable[-2] > time):
                break
            elif((time - variable[-2]) < timespan):
                timespan = time - variable[-2]
                recent_route = variable

        return recent_route

    def find_most_recent_grow_rate(self, variables, date, time):
        grow_rate = 0
        timespan = float('inf')
        variables_filter_by_date = [
            variable for variable in variables if variable[-3] == date]
        i = 0
        for variable in variables_filter_by_date:
            if(variable[-2] > time):
                break
            i += 1

        if(i >= 1):
            grow_rate = variables_filter_by_date[i-1][-1] - variables_filter_by_date[i - 2][-1]

        return grow_rate

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
        rows.sort(key=lambda row: row["time"])
        with open(filename, 'w') as csvfile:
            fieldnames = ['link_ID', 'length', 'width',
                          'link_class', 'weekday', 'date', 'time', 'travel_time']
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def _num(self, s):
        try:
            return int(s)
        except ValueError:
            return float(s)
