import os
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime


def save(name='', fmt='png'):
    i_path = './Data'.format(fmt)
    if not os.path.exists(i_path):
        os.mkdir(i_path)
    os.chdir(i_path)
    plt.savefig('{}.{}'.format(name, fmt), dpi=300)
    plt.close()


def graph(graph_name, ylabel, streamer, data):
    x = []
    y = []
    z = []

    for obj in data:
        x.append(obj[0])
        y.append(obj[1])
        z.append(obj[2])

    datetime_list = []

    length = len(y) - 1
    while length != -1:
        datetime_list.append(y[length] + '-' + z[length])
        length = length - 1

    time_info = []
    for dates in datetime_list:
        time = datetime.strptime(dates, "%Y-%m-%d-%H:%M")
        time_info.append(time)

    dates = matplotlib.dates.date2num(time_info)
    fig = plt.figure(frameon=False)
    fig.set_size_inches(16, 9)

    plt.grid(True)
    plt.title(graph_name)
    plt.xlabel('Дата (время)')
    plt.ylabel(ylabel)
    plt.plot_date(dates, x, 'go-', linewidth=2, markersize=1, label=streamer)
    plt.legend()

    save(streamer, fmt='jpg')

    plt.show()
