# Import the necessary modules and libraries
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from problem_reader import ProblemReader

def train_median_model(samples):
    links_map = set(map(lambda x: x[0], samples))
    variables_group_by_links = [
        [variable for variable in samples if variable[0] == x] for x in links_map]
    link_traval_time_median = []
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

        link_traval_time_median.append([variables_by_link[0][0],y_median, loss])

    return link_traval_time_median, total_loss

def main():

    # Read traning data set.
    from_date = "2016-03-01"
    end_date = "2016-04-30"
    reader = ProblemReader()
    variables = reader.read_variables(
        "data\\training_data\\", from_date, end_date)


    median_unfit_links_weekend = []
    median_fit_links_morning = []
    median_unfit_links_evening = []
    median_fitted_links = []
    link_traval_time_median_morning = []
    link_traval_time_median_evening = []
    link_traval_time_median_weekend = []

    loss = 0
    link_traval_time_median_all, total_loss = train_median_model(variables)
    for t in link_traval_time_median_all:
        loss += t[2]
        if(t[2] < 0.3):
            median_fitted_links.append(t[0])

    print("EMPE (All) : {}".format(total_loss / len(variables)))

    variables_morning = [v for v in variables if
                        v[-2] >= 8 and v[-2] <= 9 and v[-4] <6]
    link_traval_time_median_morning, total_loss = train_median_model(variables_morning)
    loss = 0
    for t in link_traval_time_median_morning:
        loss += t[2]
        if(t[2] < 0.3):
            median_fit_links_morning.append(t[0])

    print("EMPE (Morning) : {}".format(total_loss / len(variables_morning)))

    variables_evening = [v for v in variables if
                        v[-2] > 20 and v[-2] < 24 and v[-4] <6]
    link_traval_time_median_evening, total_loss = train_median_model(variables_evening)
    loss = 0
    for t in link_traval_time_median_evening:
        loss += t[2]
        if(t[2] > 0.3):
            median_unfit_links_evening.append(t[0])

    print("EMPE (Evening) : {}".format(total_loss / len(variables_evening)))


    variables_weekend = [v for v in variables if
                        v[-4] == 6 or v[-4] == 7]
    link_traval_time_median_weekend,total_loss = train_median_model(variables_weekend)
    loss = 0
    for t in link_traval_time_median_weekend:
        loss += t[2]
        if(t[2] > 0.3):
            median_unfit_links_weekend.append(t[0])

    print("EMPE (Weekend) : {}".format(total_loss / len(variables_weekend)))

    median_model = {}
    median_model["link_traval_time_median_weekend"] = link_traval_time_median_weekend
    median_model["median_unfit_links_weekend"] = median_unfit_links_weekend
    median_model["link_traval_time_median_evening"] = link_traval_time_median_evening
    median_model["median_unfit_links_evening"] = median_unfit_links_evening
    median_model["link_traval_time_median_morning"] = link_traval_time_median_morning
    median_model["median_fit_links_morning"] = median_fit_links_morning
    median_model["median_fitted_links"] = median_fitted_links

    # persistence model
    with open("data\\models\\median\\model", 'wb') as pickle_file:
        pickle.dump(median_model, pickle_file)

if __name__ == "__main__": main()