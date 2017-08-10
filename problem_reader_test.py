import unittest
from problem_reader import ProblemReader


class ProblemReaderTest(unittest.TestCase):
    def test_read(self):
        reader = ProblemReader()
        reader.read_link_info("data\\")
        self.assertTrue(len(reader.link_info) > 0)
        self.assertTrue(len(reader.link_top) > 0)
        self.assertTrue(reader.link_info['4377906289869500514'][0] == '57')
        self.assertTrue(
            reader.link_top['4377906284422600514'][0][0] == '3377906289434510514')

    def test_preprocess_training_data(self):
        reader = ProblemReader()
        reader.read_link_info("data\\")
        reader.preprocess_training_data("data\\test.txt")

    def test_read_variables(self):
        reader = ProblemReader()
        variables = reader.read_variables(
            "data\\training_data\\", "2016-5-21", "2016-5-21")
        self.assertTrue(len(variables) > 0)

    def test_group_variables_by_link(self):
        reader = ProblemReader()
        reader.read_link_info("data\\")
        variables = reader.read_variables(
            "data\\test\\", "2016-03-01", "2016-03-01")
        variables_group_by_link = reader.group_variables_by_link(variables)
        self.assertTrue(len(variables_group_by_link[9377906288175510514]) == 5)
        link_travel_time = variables_group_by_link[9377906288175510514]
        for i in range(len(link_travel_time)):
            if (i < (len(link_travel_time) - 2)):
                self.assertTrue(
                    link_travel_time[i + 1][-3] >= link_travel_time[i][-3])
                if(link_travel_time[i + 1][-3] == link_travel_time[i][-3]):
                    self.assertTrue(
                        link_travel_time[i + 1][-2] > link_travel_time[i][-2])
    def test_find_most_recent_grow_rate(self):
        reader = ProblemReader()
        reader.read_link_info("data\\")
        variables = reader.read_variables(
            "data\\test\\", "2016-03-01", "2016-03-01")
        variables_group_by_link = reader.group_variables_by_link(variables)
        growRate = reader.find_most_recent_grow_rate(variables_group_by_link[9377906288175510514],3.032258064516129,0.06)
        self.assertEqual(growRate,-2.3)


    def test_find_neighboring_routes(self):
        reader = ProblemReader()
        reader.read_link_info("data\\")
        variables = reader.read_variables(
            "data\\training_data\\", "2016-03-01", "2016-03-01")
        start_hour = 8
        end_hour = 9
        variables_selected = [v for v in variables if
                              v[-2] >= start_hour and v[-2] <= end_hour and v[-4] < 6]

        variables_recent = [v for v in variables if
                            v[-2] >= start_hour - 2 and v[-2] < start_hour and v[-4] < 6]

        variables_recent_group_by_links = reader.group_variables_by_link(
            variables_recent)
        variables_group_by_links = reader.group_variables_by_link(
            variables_selected)

        for link, routes in variables_group_by_links.items():
            recent_neighboring_routes = reader.find_neighboring_routes(
                variables_recent_group_by_links, routes[0][0], routes[0][-3], routes[0][-2])
            in_link = int(reader.link_top[str(link)][0])
            out_link = int(reader.link_top[str(link)][-1])
            if(link == 3377906280028510514):
                self.assertTrue(recent_neighboring_routes[0][0] == 4377906282541600514)
                self.assertTrue(recent_neighboring_routes[0][-1] == 76.6)
                self.assertTrue(recent_neighboring_routes[0][-2] > 7.9)

            if len(recent_neighboring_routes) > 0:
                self.assertTrue(recent_neighboring_routes[0][0] == in_link 
                    or recent_neighboring_routes[0][0] == out_link)

            if len(recent_neighboring_routes) > 1:
                self.assertTrue(recent_neighboring_routes[1][0] == out_link
                    or recent_neighboring_routes[0][0] == in_link)


if __name__ == '__main__':
    unittest.main()
