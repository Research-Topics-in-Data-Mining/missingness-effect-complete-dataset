import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


def determine_tuple(tup_perm: tuple, t: int, l: int, x: int):
    tup = ()
    match tup_perm:
        case (0, 1, 2):
            tup = (t, l, x)
        case (0, 2, 1):
            tup = (t, x, l)
        case (1, 0, 2):
            tup = (l, t, x)
        case (1, 2, 0):
            tup = (l, x, t)
        case (2, 0, 1):
            tup = (x, t, l)
        case (2, 1, 0):
            tup = (x, l, t)
    return tup


def determine_order(t: str, l: str, x: str):
    tup = ()
    match (t, l, x):
        case ("MCAR", "MAR", "MNAR"):
            tup = (0, 1, 2)
        case ("MCAR", "MNAR", "MAR"):
            tup = (0, 2, 1)
        case ("MAR", "MCAR", "MNAR"):
            tup = (1, 0, 2)
        case ("MAR", "MNAR", "MCAR"):
            tup = (2, 0, 1)
        case ("MNAR", "MCAR", "MAR"):
            tup = (1, 2, 0)
        case ("MNAR", "MAR", "MCAR"):
            tup = (2, 1, 0)
    return tup


def barplot_type1(dic_m, dic_s, x_axis_miss_type: str, legend_miss_type: str, title_miss_type: str, percentage: int, column: int):
    tup_perm = determine_order(
        title_miss_type, legend_miss_type, x_axis_miss_type)

    light = []
    medium = []
    dark = []
    # For data for different plots, just change the miss_p and range list.
    for t in [percentage]:
        for idx_2, l in enumerate([0, 10, 20]):
            aux = [0] * 3
            for idx_1, x in enumerate([0, 10, 20]):
                if t == 0 and l == 0 and x == 0:
                    continue
                tup = determine_tuple(tup_perm, t, l, x)
                # print(tup)
                aux[idx_1] = dic_m[tup][column]

            if idx_2 == 0:
                light = aux
            elif idx_2 == 1:
                medium = aux
            else:
                dark = aux

    # print("l: ", np.around(light, decimals=6))
    # print("m: ", np.around(medium, decimals=6))
    # print("d: ", np.around(dark, decimals=6))

    # x axis label
    x_label = x_axis_miss_type
    # y axis label
    y_label = "mean"
    # plot title
    plot_title = title_miss_type + " " + str(percentage)
    # legend title
    legend_title = legend_miss_type

    N = 3
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects_light = ax.bar(ind, light, width, color='skyblue')
    rects_medium = ax.bar(ind+width, medium, width, color='dodgerblue')
    rects_dark = ax.bar(ind+width*2, dark, width, color='navy')

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('0%', '10%', '20%'))
    ax.legend((rects_light[0], rects_medium[0], rects_dark[0]),
              ('0%', '10%', '20%'), title=legend_title)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.005*h, '%.4f' % float(h),
                    ha='center', va='bottom')

    autolabel(rects_light)
    autolabel(rects_medium)
    autolabel(rects_dark)

    plt.ylim([0.09, 0.1])
    plt.title(plot_title)
    plt.show()


def barplot_type3(dic_m):
    for mcar_p in [0, 10, 20]:
        # plt.figure(figsize=[15,14])
        for mar_p, marker in zip([0, 10, 20], ["s", "x", "o"]):
            for mnar_p, color in zip([0, 10, 20], ["blue", "green", "red"]):
                if mcar_p == 0 and mar_p == 0 and mnar_p == 0:
                    continue
                x = dic_m[(mcar_p, mar_p, mnar_p)][4]
                y = dic_m[(mcar_p, mar_p, mnar_p)][1]
                label = "MAR=" + str(mar_p) + ", MNAR=" + str(mnar_p)
                plt.scatter(x, y, marker=marker, c=color, s=60, label=label)

        plt.axhline(y=0.0, color='black', linestyle='-')
        plt.ylabel("bias")
        plt.xlabel("accuracy_a")
        plt.title("MCAR=" + str(mcar_p))
        plt.legend(loc='upper left', bbox_to_anchor=(1.04, 1))
        plt.tight_layout()

        plt.show()
        plt.clf()
