# Import the necessary modules and libraries
import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from problem_reader import ProblemReader

# Median model
model_file = "data\\models\\median\\model"
model_median = None
with open(model_file, 'rb') as pickle_file:
    model_median = pickle.load(pickle_file)

# Model
model_file = "data\\models\\2016-03-01TO2016-03-31"
models = None
with open(model_file, 'rb') as pickle_file:
    models = pickle.load(pickle_file)

# Read validation data set.
from_date = "2016-04-01"
end_date = "2016-04-30"
reader = ProblemReader()
variables = reader.read_variables(
    "data\\training_data\\", from_date, end_date)

start_hour = 8
end_hour = 9

variables_selected = [v for v in variables if
                      v[-2] >= start_hour and v[-2] <= end_hour and v[-4] < 6
                      and v[0] not in model_median["median_fit_links_morning"]]

links_map = set(map(lambda x: x[0], variables_selected))
variables_group_by_links = [
    [variable for variable in variables_selected if variable[0] == x] for x in links_map]

total_loss = 0
for variables_by_link in variables_group_by_links:
    variables_array = np.array(variables_by_link)
    y = variables_array[:, -1]
    X = np.delete(variables_array, np.s_[-1:], 1)
    X = np.delete(X, np.s_[0:-3], 1)
    X = np.delete(X, np.s_[-2:-1], 1)
    model = models[variables_by_link[0][0]]
    y_hat = model.predict(X)
    for i in range(len(y_hat)):
        total_loss += abs(y_hat[i] - y[i]) / y[i]

loss = total_loss / len(variables_selected)

print("MAPE of the model: {}".format(loss))
