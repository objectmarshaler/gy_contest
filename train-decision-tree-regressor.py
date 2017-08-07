# Import the necessary modules and libraries
import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from problem_reader import ProblemReader

# Read training data set.
from_date = "2016-03-05"
end_date = "2016-03-06"
reader = ProblemReader()
variables = np.array(reader.read_variables(
    "data\\training_data\\", from_date, end_date))
y = variables[:, -1]
X = np.delete(variables, np.s_[-1:], 1)

# Fit regression model
regr = DecisionTreeRegressor()
regr.fit(X, y)

# persistence model
with open("data\\models\\" + from_date + "TO" + end_date, 'wb') as pickle_file:
    pickle.dump(regr, pickle_file)
