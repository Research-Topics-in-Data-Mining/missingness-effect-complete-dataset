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
    if column == 0:
        barplot_type1_mean(dic_m, dic_s, x_axis_miss_type, legend_miss_type, title_miss_type, percentage)
    elif column == 1:
        barplot_type1_bias(dic_m, dic_s, x_axis_miss_type, legend_miss_type, title_miss_type, percentage)
    elif column == 3:
        barplot_type1_std(dic_m, dic_s, x_axis_miss_type, legend_miss_type, title_miss_type, percentage)
    elif column == 4:
        barplot_type1_acc_a(dic_m, dic_s, x_axis_miss_type, legend_miss_type, title_miss_type, percentage)
    elif column == 5:
        barplot_type1_acc_b(dic_m, dic_s, x_axis_miss_type, legend_miss_type, title_miss_type, percentage)


# Bar plot for the mean.
def barplot_type1_mean(dic_m, dic_s, x_axis_miss_type: str, legend_miss_type: str, title_miss_type: str, percentage: int):
    tup_perm = determine_order(
    title_miss_type, legend_miss_type, x_axis_miss_type)

    light_m = []
    medium_m = []
    dark_m = []
    light_s = []
    medium_s = []
    dark_s = []
    for t in [percentage]:
        for idx_2, l in enumerate([0, 10, 20]):
            aux_m = [0] * 3
            aux_s = [0] * 3
            for idx_1, x in enumerate([0, 10, 20]):
                if t == 0 and l == 0 and x == 0:
                    continue
                tup = determine_tuple(tup_perm, t, l, x)
                aux_m[idx_1] = dic_m[tup][0]
                aux_s[idx_1] = dic_s[tup][0]

            if idx_2 == 0:
                light_m = aux_m
                light_s = aux_s
            elif idx_2 == 1:
                medium_m = aux_m
                medium_s = aux_s
            else:
                dark_m = aux_m
                dark_s = aux_s

    # x axis label
    x_label = x_axis_miss_type
    # y axis label
    y_label = "sample mean"
    # plot title
    plot_title = title_miss_type + " " + str(percentage) + "%"
    # legend title
    legend_title = legend_miss_type

    N = 3
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.yaxis.grid(linewidth=0.5)

    rects_light_m = ax.bar(x=ind, height=light_m, width=width, color='skyblue', yerr=light_s, capsize = 10)
    rects_medium_m = ax.bar(x=ind+width, height=medium_m, width=width, color='dodgerblue', yerr=medium_s, capsize = 10)
    rects_dark_m = ax.bar(x=ind+width*2, height=dark_m, width=width, color='midnightblue', yerr=dark_s, capsize = 10)

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('0%', '10%', '20%'))
    ax.legend((rects_light_m[0], rects_medium_m[0], rects_dark_m[0]),
              ('0%', '10%', '20%'), title=legend_title)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.007*h, '%.4f' % float(h),
                    ha='center', va='bottom')

    autolabel(rects_light_m)
    autolabel(rects_medium_m)
    autolabel(rects_dark_m)

    plt.axhline(y=0.0963602811950791, color='grey', linestyle=':')
    plt.text(2, 0.0965, "true sample mean")
    
    plt.ylim([0.09, 0.1])
    plt.title(plot_title)
    plt.show()


# Bar plot for the bias.
def barplot_type1_bias(dic_m, dic_s, x_axis_miss_type: str, legend_miss_type: str, title_miss_type: str, percentage: int):
    tup_perm = determine_order(
    title_miss_type, legend_miss_type, x_axis_miss_type)

    light_m = []
    medium_m = []
    dark_m = []
    light_s = []
    medium_s = []
    dark_s = []
    for t in [percentage]:
        for idx_2, l in enumerate([0, 10, 20]):
            aux_m = [0] * 3
            aux_s = [0] * 3
            for idx_1, x in enumerate([0, 10, 20]):
                if t == 0 and l == 0 and x == 0:
                    continue
                tup = determine_tuple(tup_perm, t, l, x)
                aux_m[idx_1] = dic_m[tup][1]
                aux_s[idx_1] = dic_s[tup][1]

            if idx_2 == 0:
                light_m = aux_m
                light_s = aux_s
            elif idx_2 == 1:
                medium_m = aux_m
                medium_s = aux_s
            else:
                dark_m = aux_m
                dark_s = aux_s

    # x axis label
    x_label = x_axis_miss_type
    # y axis label
    y_label = "bias"
    # plot title
    plot_title = title_miss_type + " " + str(percentage) + "%"
    # legend title
    legend_title = legend_miss_type

    N = 3
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.yaxis.grid(linewidth=0.5)

    rects_light_m = ax.bar(x=ind, height=light_m, width=width, color='skyblue', yerr=light_s, capsize = 10)
    rects_medium_m = ax.bar(x=ind+width, height=medium_m, width=width, color='dodgerblue', yerr=medium_s, capsize = 10)
    rects_dark_m = ax.bar(x=ind+width*2, height=dark_m, width=width, color='midnightblue', yerr=dark_s, capsize = 10)

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('0%', '10%', '20%'))
    ax.legend((rects_light_m[0], rects_medium_m[0], rects_dark_m[0]),
              ('0%', '10%', '20%'), title=legend_title)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.35*h, '%.4f' % float(h),
                    ha='center', va='top')

    autolabel(rects_light_m)
    autolabel(rects_medium_m)
    autolabel(rects_dark_m)

    plt.axhline(y=0.0, color='grey', linestyle=':')
    
    plt.ylim([-0.01, 0.0])
    plt.title(plot_title)
    plt.show()


# Bar plot for sample standard deviation.
def barplot_type1_std(dic_m, dic_s, x_axis_miss_type: str, legend_miss_type: str, title_miss_type: str, percentage: int):
    tup_perm = determine_order(
    title_miss_type, legend_miss_type, x_axis_miss_type)

    light_m = []
    medium_m = []
    dark_m = []
    light_s = []
    medium_s = []
    dark_s = []
    for t in [percentage]:
        for idx_2, l in enumerate([0, 10, 20]):
            aux_m = [0] * 3
            aux_s = [0] * 3
            for idx_1, x in enumerate([0, 10, 20]):
                if t == 0 and l == 0 and x == 0:
                    continue
                tup = determine_tuple(tup_perm, t, l, x)
                aux_m[idx_1] = dic_m[tup][3]
                aux_s[idx_1] = dic_s[tup][3]

            if idx_2 == 0:
                light_m = aux_m
                light_s = aux_s
            elif idx_2 == 1:
                medium_m = aux_m
                medium_s = aux_s
            else:
                dark_m = aux_m
                dark_s = aux_s

    # x axis label
    x_label = x_axis_miss_type
    # y axis label
    y_label = "sample standard deviation"
    # plot title
    plot_title = title_miss_type + " " + str(percentage) + "%"
    # legend title
    legend_title = legend_miss_type

    N = 3
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.yaxis.grid(linewidth=0.5)

    rects_light_m = ax.bar(x=ind, height=light_m, width=width, color='skyblue', yerr=light_s, capsize = 10)
    rects_medium_m = ax.bar(x=ind+width, height=medium_m, width=width, color='dodgerblue', yerr=medium_s, capsize = 10)
    rects_dark_m = ax.bar(x=ind+width*2, height=dark_m, width=width, color='midnightblue', yerr=dark_s, capsize = 10)

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('0%', '10%', '20%'))
    ax.legend((rects_light_m[0], rects_medium_m[0], rects_dark_m[0]),
              ('0%', '10%', '20%'), title=legend_title)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.04*h, '%.4f' % float(h),
                    ha='center', va='bottom')

    autolabel(rects_light_m)
    autolabel(rects_medium_m)
    autolabel(rects_dark_m)

    plt.axhline(y=0.01406412813767362, color='grey', linestyle=':')
    plt.text(2.55, 0.015, "true sample std")
    
    plt.ylim([0.0, 0.05])
    plt.title(plot_title)
    plt.show()


# Bar plot for accuracy_a.
def barplot_type1_acc_a(dic_m, dic_s, x_axis_miss_type: str, legend_miss_type: str, title_miss_type: str, percentage: int):    
    tup_perm = determine_order(
    title_miss_type, legend_miss_type, x_axis_miss_type)

    light_m = []
    medium_m = []
    dark_m = []
    light_s = []
    medium_s = []
    dark_s = []
    for t in [percentage]:
        for idx_2, l in enumerate([0, 10, 20]):
            aux_m = [0] * 3
            aux_s = [0] * 3
            for idx_1, x in enumerate([0, 10, 20]):
                if t == 0 and l == 0 and x == 0:
                    continue
                tup = determine_tuple(tup_perm, t, l, x)
                aux_m[idx_1] = dic_m[tup][4]
                aux_s[idx_1] = dic_s[tup][4]

            if idx_2 == 0:
                light_m = aux_m
                light_s = aux_s
            elif idx_2 == 1:
                medium_m = aux_m
                medium_s = aux_s
            else:
                dark_m = aux_m
                dark_s = aux_s

    # x axis label
    x_label = x_axis_miss_type
    # y axis label
    y_label = "accuracy_a"
    # plot title
    plot_title = title_miss_type + " " + str(percentage) + "%"
    # legend title
    legend_title = legend_miss_type

    N = 3
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.yaxis.grid(linewidth=0.5)

    rects_light_m = ax.bar(x=ind, height=light_m, width=width, color='skyblue', yerr=light_s, capsize = 10)
    rects_medium_m = ax.bar(x=ind+width, height=medium_m, width=width, color='dodgerblue', yerr=medium_s, capsize = 10)
    rects_dark_m = ax.bar(x=ind+width*2, height=dark_m, width=width, color='midnightblue', yerr=dark_s, capsize = 10)

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('0%', '10%', '20%'))
    ax.legend((rects_light_m[0], rects_medium_m[0], rects_dark_m[0]),
              ('0%', '10%', '20%'), title=legend_title)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.035*h, '%.4f' % float(h),
                    ha='center', va='bottom')

    autolabel(rects_light_m)
    autolabel(rects_medium_m)
    autolabel(rects_dark_m)

    plt.axhline(y=0.935672514619883, color='grey', linestyle=':')
    plt.text(2.55, 0.938, "true accuracy")
    
    plt.ylim([0.8, 1.0])
    plt.title(plot_title)
    plt.show()

    
# Bar plot for accuracy_b.
def barplot_type1_acc_b(dic_m, dic_s, x_axis_miss_type: str, legend_miss_type: str, title_miss_type: str, percentage: int):
    tup_perm = determine_order(
    title_miss_type, legend_miss_type, x_axis_miss_type)

    light_m = []
    medium_m = []
    dark_m = []
    light_s = []
    medium_s = []
    dark_s = []
    for t in [percentage]:
        for idx_2, l in enumerate([0, 10, 20]):
            aux_m = [0] * 3
            aux_s = [0] * 3
            for idx_1, x in enumerate([0, 10, 20]):
                if t == 0 and l == 0 and x == 0:
                    continue
                tup = determine_tuple(tup_perm, t, l, x)
                aux_m[idx_1] = dic_m[tup][5]
                aux_s[idx_1] = dic_s[tup][5]

            if idx_2 == 0:
                light_m = aux_m
                light_s = aux_s
            elif idx_2 == 1:
                medium_m = aux_m
                medium_s = aux_s
            else:
                dark_m = aux_m
                dark_s = aux_s

    # x axis label
    x_label = x_axis_miss_type
    # y axis label
    y_label = "accuracy_b"
    # plot title
    plot_title = title_miss_type + " " + str(percentage) + "%"
    # legend title
    legend_title = legend_miss_type

    N = 3
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.yaxis.grid(linewidth=0.5)

    rects_light_m = ax.bar(x=ind, height=light_m, width=width, color='skyblue', yerr=light_s, capsize = 10)
    rects_medium_m = ax.bar(x=ind+width, height=medium_m, width=width, color='dodgerblue', yerr=medium_s, capsize = 10)
    rects_dark_m = ax.bar(x=ind+width*2, height=dark_m, width=width, color='midnightblue', yerr=dark_s, capsize = 10)

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('0%', '10%', '20%'))
    ax.legend((rects_light_m[0], rects_medium_m[0], rects_dark_m[0]),
              ('0%', '10%', '20%'), title=legend_title)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.017*h, '%.4f' % float(h),
                    ha='center', va='bottom')

    autolabel(rects_light_m)
    autolabel(rects_medium_m)
    autolabel(rects_dark_m)

    plt.axhline(y=0.935672514619883, color='grey', linestyle=':')
    plt.text(2.55, 0.938, "true accuracy")
    
    plt.ylim([0.8, 1.0])
    plt.title(plot_title)
    plt.show()


# Scatter plot for bias and accuracy.
def barplot_type3(dic_m, true_acc):
    for mcar_p in [0, 10, 20]:
        for mar_p, marker in zip([0, 10, 20], ["s", "x", "o"]):
            for mnar_p, color in zip([0, 10, 20], ["blue", "green", "red"]):
                if mcar_p == 0 and mar_p == 0 and mnar_p == 0:
                    continue
                x = dic_m[(mcar_p, mar_p, mnar_p)][5]
                y = dic_m[(mcar_p, mar_p, mnar_p)][1]
                label = "MAR=" + str(mar_p) + ", MNAR=" + str(mnar_p)
                plt.scatter(x, y, marker=marker, c=color, s=60, label=label)
        x = [true_acc]
        y = [0.0]
        plt.scatter(x, y, marker="*", c="black", s=100, label="no missingness")
        plt.axhline(y=0.0, color='black', linestyle='-')
        plt.ylabel("bias")
        plt.xlabel("accuracy_b")
        plt.title("MCAR=" + str(mcar_p))
        plt.legend(loc='upper left', bbox_to_anchor=(1.04, 1))
        plt.tight_layout()

        plt.show()
        plt.clf()
