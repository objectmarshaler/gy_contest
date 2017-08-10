# Import the necessary modules and libraries
import numpy as np
import pickle
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import train_model_utility as utility

def train(model_median, reader,from_date,end_date):
   
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

    models_dict = {}
    variables_recent_group_by_links = reader.group_variables_by_link(
        variables_recent)
    variables_group_by_links = reader.group_variables_by_link(
        variables_selected)

    for link, variables_by_link in variables_group_by_links.items():

        # Fit regression model
        #regr = RandomForestRegressor(n_estimators=200)
        X,y = utility.generate_variable(reader, variables_by_link,
                              variables_recent_group_by_links, model_median)
        regr = DecisionTreeRegressor(max_depth=2000)
        regr.fit(X, y)
        models_dict[link] = regr

    # persistence model
    with open("data\\models\\" + from_date + "TO" + end_date, 'wb') as pickle_file:
        pickle.dump(models_dict, pickle_file)
    
    return models_dict

