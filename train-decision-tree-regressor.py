# Import the necessary modules and libraries
import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from problem_reader import ProblemReader

# Median model
model_file = "data\\models\\median\\model"
model_median = None
with open(model_file, 'rb') as pickle_file:
    model_median = pickle.load(pickle_file)

# Read training data set.
from_date = "2016-03-01"
end_date = "2016-03-31"
reader = ProblemReader()
variables = reader.read_variables(
    "data\\training_data\\", from_date, end_date)

start_hour = 8
end_hour = 9

variables_selected = [v for v in variables if
                      v[-2] >= start_hour and v[-2] <= end_hour and v[-4] < 6 
                      and v[0] not in model_median["median_fit_links_morning"]]

models_dict = {}
links_map = set(map(lambda x: x[0], variables_selected))
variables_group_by_links = [
    [variable for variable in variables_selected if variable[0] == x] for x in links_map]

for variables_by_link in variables_group_by_links:
    variables_array = np.array(variables_by_link)
    y = variables_array[:, -1]
    X = np.delete(variables_array, np.s_[-1:], 1)
    X = np.delete( X, np.s_[0:-3], 1)
    X = np.delete( X, np.s_[-2:-1], 1)
    # Fit regression model
    #regr = RandomForestRegressor(n_estimators=200)
    regr = DecisionTreeRegressor()
    regr.fit(X, y)
    models_dict[variables_by_link[0][0]] = regr

# persistence model
with open("data\\models\\" + from_date + "TO" + end_date, 'wb') as pickle_file:
    pickle.dump(models_dict, pickle_file)
