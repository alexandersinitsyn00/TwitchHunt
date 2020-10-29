import os
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime


def save(name='', fmt='png'):
    plt.savefig('./Data/{}.{}'.format(name, fmt), dpi=300)


def datetime_graph(graph_name, ylabel, streamer, data):
    y = []
    x = []

    for row in data:
        x.append(row[0])
        y.append(datetime.strptime(f'{row[1]}-{row[2]}', "%Y-%m-%d-%H:%M"))
    y = matplotlib.dates.date2num(y)

    fig = plt.figure(frameon=False)
    fig.set_size_inches(16, 9)

    plt.grid(True)
    plt.title(graph_name)
    plt.xlabel('Дата (время)')
    plt.ylabel(ylabel)

    plt.plot_date(y, x, 'go-', linewidth=2, markersize=1, label=streamer)
    plt.legend()

    save(streamer, fmt='jpg')
