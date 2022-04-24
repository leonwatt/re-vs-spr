from cProfile import label
from smtplib import LMTP
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def format_percentage(value):
    return f"{round(value * 100)}%"

def generate_values(data, x, y = None, count_y = False, display_percentage = False, display_absolute_value = False, sort_by = None, sort_desc=False):
    data = list(data)

    x_func = x if callable(x) else lambda a: a[x]
    y_func = y if callable(y) else lambda a: a[y]
    
    if count_y:
        counts = {}
        for d in data:
            x_val = x_func(d)
            counts.setdefault(x_val, 0)
            counts[x_val] += 1
        x_vals = list(counts.keys())
        y_vals = list(counts.values())
    else:
        x_vals = [x_func(d) for d in data]
        y_vals = [y_func(d) for d in data]

    if display_percentage or display_absolute_value:
        y_sum = sum(y_vals)
        def display_value(index):
            arr = []
            if display_absolute_value: arr.append(y_vals[index])
            if display_percentage: arr.append(format_percentage(y_vals[index] / y_sum))
            return ": ".join([str(el) for el in arr])
        x_vals = [f"{v} ({display_value(i)})" for (i, v) in enumerate(x_vals)]

    if sort_by != None:
        pairs = [(x_val, y_vals[i]) for (i, x_val) in enumerate(x_vals)]
        pairs = sorted(pairs, key=lambda pair: pair[0] if sort_by == "x" else pair[1], reverse=sort_desc)
        x_vals = [p[0] for p in pairs]
        y_vals = [p[1] for p in pairs]

    return (x_vals, y_vals)

def count_y(dataset, transformation=lambda x: x):
    (keys, values) = generate_values(dataset, x=transformation, count_y=True)
    res = {}
    for (i, k) in enumerate(keys):
        res[k] = values[i]
    return res

def pie(data, x, y = None, count_y = False, display_percentage = False, display_absolute_value = False, sort_by = None, sort_desc=True, title = None, hide_labels = False, save_to = None):
    fig, ax = plt.subplots(figsize=(10, 7))
    mpl.style.use("seaborn")

    x_vals, y_vals = generate_values(data, x, y, count_y, display_percentage, display_absolute_value, sort_by, sort_desc)

    ax.set_title(title)
    ax.pie(
        y_vals,
        labels=x_vals if not hide_labels else None,
        counterclock=False,
        startangle=90
    )

    if save_to != None:
        fig.savefig(save_to)

def bar(data, x, y = None, count_y = False, display_percentage = False, display_absolute_value = False, sort_by = None, sort_desc=False, size = None, title = None, hide_labels = False, x_label_rotation = 0, only_nth_x_label = 1, save_to = None):
    fig, ax = plt.subplots(figsize=size)
    mpl.style.use("seaborn")

    x_vals, y_vals = generate_values(data, x, y, count_y, display_percentage, display_absolute_value, sort_by, sort_desc)

    ax.set_title(title)
    ax.bar(
        x=x_vals,
        height=y_vals
    )

    if hide_labels:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.xticks(rotation=x_label_rotation)

    if only_nth_x_label > 1:
        all_labels = ax.get_xticklabels()
        visible_labels = all_labels[::only_nth_x_label]
        hidden_labels = [l for l in all_labels if l not in visible_labels]
        plt.setp(hidden_labels, visible=False)

    if save_to != None:
        fig.savefig(save_to)

def line_plot(data, x, y = None, count_y = False, display_percentage = False, display_absolute_value = False, sort_by = None, sort_desc=False, size = None, title = None, hide_labels = False, x_label_rotation = 0, only_nth_x_label = 1, save_to = None):
    fig, ax = plt.subplots(figsize=size)
    mpl.style.use("seaborn")

    x_vals, y_vals = generate_values(data, x, y, count_y, display_percentage, display_absolute_value, sort_by, sort_desc)

    ax.set_title(title)
    ax.plot(
        x_vals,
        y_vals
    )

    if hide_labels:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.xticks(rotation=x_label_rotation)

    if only_nth_x_label > 1:
        all_labels = ax.get_xticklabels()
        visible_labels = all_labels[::only_nth_x_label]
        hidden_labels = [l for l in all_labels if l not in visible_labels]
        plt.setp(hidden_labels, visible=False)

    if save_to != None:
        fig.savefig(save_to)


def box_plot(data, x, size = None, title = None, hide_labels = False, x_tick_labels = None, as_violin = False, save_to = None):
    fig, ax = plt.subplots(figsize=size)
    mpl.style.use("seaborn")

    if (type(data[0]) == list):
        x_vals = [generate_values(d, x, count_y=True)[0] for d in data]
    else:
        x_vals = generate_values(data, x, count_y=True)[0]

    ax.set_title(title)
    
    if as_violin: 
        ax.violinplot(x_vals, showmedians=True)
    else: ax.boxplot(x_vals)

    if x_tick_labels != None:
        if as_violin:
            x_tick_labels = [""] + x_tick_labels
        ax.set_xticklabels(x_tick_labels)

    if hide_labels:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.xticks()

    if save_to != None:
        fig.savefig(save_to)



# violin_plot([[1,2,2,3], [2,2,2,2,2,1]], x=lambda a: a, save_to="test.png", x_tick_labels=["A", "B"])