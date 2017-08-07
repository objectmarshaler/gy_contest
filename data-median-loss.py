# Import the necessary modules and libraries
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from problem_reader import ProblemReader

# Model
model_file = "data\\models\\2016-03-01TO2016-03-2"
model = None
with open(model_file, 'rb') as pickle_file:
    model = pickle.load(pickle_file)

# Read validation data set.
from_date = "2016-03-12"
end_date = "2016-06-01"
start_hour = 20
end_hour = 24
reader = ProblemReader()
variables = reader.read_variables(
    "data\\training_data\\", from_date, end_date)


unfit_links = []
fitted_links = []


# variables_0_to_5am = [v for v in variables if
#                     v[-2] > start_hour and v[-2] < end_hour and v[0] not in unfit_links]

#variables_0_to_5am = [v for v in variables if
#                     v[-4] == 4 or v[-4] == 5 and v[0] not in unfit_links]

variables_0_to_5am = [v for v in variables]

links_map = set(map(lambda x: x[0], variables_0_to_5am))
variables_group_by_links = [
    [variable for variable in variables_0_to_5am if variable[0] == x] for x in links_map]

total_loss = 0
for variables_by_link in variables_group_by_links:
    variables_array = np.array(variables_by_link)
    y = variables_array[:, -1]
    X = np.delete(variables_array, np.s_[-1:], 1)
    y_median = np.median(y)
    loss = 0
    for i in range(len(y)):
        loss += abs(y_median - y[i]) / y[i]

    total_loss += loss
    loss = loss / len(y)

    if loss > 0.5:
        unfit_links.append(variables_by_link[0][0])
    elif loss < 0.3:
        fitted_links.append(variables_by_link[0][0])
        #plt.plot(variables_array[:, -2],y)
        # plt.show()
    print("MAPE of the median evaluator({:19}): {}".format(
        variables_by_link[0][0], loss))

print("MAPE(total):{}".format(total_loss / len(variables_0_to_5am)))
print("Unfitted links:")
for l in unfit_links:
    print("{:19}".format(l))

print("Fitted links:")
for l in fitted_links:
    print("{:19}".format(l))
