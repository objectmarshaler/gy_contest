# Import the necessary modules and libraries
import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from problem_reader import ProblemReader


def generate_variable(reader, variables_by_link, recent_link_travel_time, model_median):

    for route in variables_by_link:
        link = route[0]
        neighboring_routes = reader.find_neighboring_routes(
            recent_link_travel_time, route[0], route[-3], route[-2])
        in_link = int(reader.link_top[str(link)][0])
        out_link = int(reader.link_top[str(link)][-1])
        if len(neighboring_routes) > 0 and neighboring_routes[0][0] == in_link:
            route.insert(-1, neighboring_routes[0][-1])
        else:
            route.insert(-1,
                         model_median["link_traval_time_median_morning"][in_link][1])

        if len(neighboring_routes) == 2:
            route.insert(-1, neighboring_routes[1][-1])
        elif len(neighboring_routes) == 1 and neighboring_routes[0][0] == out_link:
            route.insert(-1, neighboring_routes[0][-1])
        else:
            route.insert(-1,
                         model_median["link_traval_time_median_morning"][out_link][1])

        growRate = reader.find_most_recent_grow_rate(
            recent_link_travel_time[link], route[-3], route[-2])
        route.insert(-1, growRate)

    variables_array = np.array(variables_by_link)
    y = variables_array[:, -1]
    X = np.delete(variables_array, np.s_[-1:], 1)
    X = np.delete(X, np.s_[0:-6], 1)
    return X, y

def generate_variable1(reader, variables_by_link, recent_link_travel_time, model_median):
    for route in variables_by_link:
        link = route[0]
        growRate = reader.find_most_recent_grow_rate(
            recent_link_travel_time[link], route[-3], route[-2])
        route.insert(-1, growRate)
    variables_array = np.array(variables_by_link)
    y = variables_array[:, -1]
    X = np.delete(variables_array, np.s_[-1:], 1)
    X = np.delete(X, np.s_[0:-4], 1)
    return X, y

def test_model(model, X, y):
    y_hat = model.predict(X)
    loss = 0
    for i in range(len(y_hat)):
        loss += abs(y_hat[i] - y[i]) / y[i]
    return loss


def test_model_with_link_travel_time(model_median, models, reader, from_date, end_date):

    reader.read_link_info("data\\")
    variables = reader.read_variables(
        "data\\training_data\\", from_date, end_date)

    start_hour = 8
    end_hour = 9

    variables_selected = [v for v in variables if
                          v[-2] >= start_hour and v[-2] <= end_hour and v[-4] < 6
                          and v[0] not in model_median["median_fit_links_morning"]]

    variables_recent = [v for v in variables if
                        v[-2] >= start_hour -
                        2 and v[-2] < start_hour and v[-4] < 6
                        and v[0] not in model_median["median_fit_links_morning"]]

    variables_recent_group_by_links = reader.group_variables_by_link(
        variables_recent)
    variables_group_by_links = reader.group_variables_by_link(
        variables_selected)

    total_loss = 0
    for link, variables_by_link in variables_group_by_links.items():

        # Fit regression model
        #regr = RandomForestRegressor(n_estimators=200)
        X, y = generate_variable(reader, variables_by_link,
                                 variables_recent_group_by_links, model_median)
        model = models[variables_by_link[0][0]]
        link_loss = test_model(model, X, y)
        total_loss += link_loss

    loss = total_loss / len(variables_selected)

    print("MAPE of the model: {}".format(loss))
