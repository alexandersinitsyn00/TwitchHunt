import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib


def save_to_dir(abs_path):
    print(abs_path)
    plt.savefig(abs_path, dpi=300)


def save_datetime_graph(graph_name, y_label, abs_path, data, channel):
    y = []
    x = []

    for row in data:
        x.append(row[0])
        y.append(datetime.strptime(f'{row[1]}', "%Y-%m-%d %H:%M"))

    y = matplotlib.dates.date2num(y)

    fig = plt.figure(frameon=False)
    fig.set_size_inches(16, 9)

    plt.grid(True)
    plt.title(graph_name)
    plt.xlabel('Дата (время)')
    plt.ylabel(y_label)

    plt.plot_date(y, x, 'go-', linewidth=2, markersize=1, label=channel)
    plt.legend()

    save_to_dir(abs_path)
