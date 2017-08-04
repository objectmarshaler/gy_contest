#Import the necessary modules and libraries
import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from problem_reader import ProblemReader

# Model
model_file = "data\\models\\2016-03-01TO2016-03-31"
model = None
with open(model_file, 'rb') as pickle_file:
    model = pickle.load(pickle_file)

# Read validation data set.
from_date = "2016-04-01"
end_date = "2016-04-15"
reader = ProblemReader()
variables = np.array(reader.read_variables(
    "data\\training_data\\", from_date, end_date))

# Create a random dataset
y = variables[:, -1]
X = np.delete(variables, np.s_[-1:], 1)

# Test
y_hat = model.predict(X)

loss = 0
for i in range(len(y_hat)):
    loss += abs(y_hat[i] - y[i])/y[i]

loss = loss/len(y_hat)

print("MAPE of the model: {}".format(loss))