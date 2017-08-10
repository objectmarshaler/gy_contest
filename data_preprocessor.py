from problem_reader import ProblemReader

reader = ProblemReader()
reader.read_link_info("data\\")
reader.preprocess_training_data("data\\gy_contest_link_traveltime_training_data.txt")