from problem_reader import ProblemReader
import matplotlib.pyplot as plt
import numpy as np


reader = ProblemReader()
variables = reader.read_variables("data\\training_data\\","2016-03-01","2016-03-02")
links_map = set(map(lambda x:x[0], variables))
variables_group_by_links = [[variable for variable in variables if variable[0]==x] for x in links_map]
fig,axs = plt.subplots(20,1)
for i in range(20):
    time, travel_time,weekday = [],[],[]
    for v in variables_group_by_links[i]:
        time.append(v[6])
        weekday.append(v[4])
        travel_time.append(v[7])
    ax = axs[i]
    ax.plot(time, travel_time)
    ax.set_title(variables_group_by_links[i][0][0])
    ax.grid(True)

plt.show()