# Import the necessary modules and libraries
import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from problem_reader import ProblemReader
import train_model_utility as utility
import train_decision_tree_regressor as trainer

# Median model
model_file = "data\\models\\median\\model"
model_median = None
with open(model_file, 'rb') as pickle_file:
    model_median = pickle.load(pickle_file)


reader = ProblemReader()
reader.read_link_info("data\\")
models = trainer.train(model_median, reader,"2016-03-01","2016-03-15")
utility.test_model_with_link_travel_time(model_median,models,reader,"2016-03-16","2016-03-31")

