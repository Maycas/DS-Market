import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def autopct_generator(limit):
    """
    Hides percentages in bar charts given a specific 'limit'
    """
    def inner_autopct(pct):
        return ('%.0f%%' % pct) if pct > limit else ''
    return inner_autopct


def get_new_labels(values, labels, limit):
    """
    Returns a list of labels only if they exceed a specific 'limit'
    given 'values' and 'labels' lists for a pie chart
    """
    return [label if value > limit / 100 else '' for value, label in zip(values, labels)]


def add_subplot(df, column, plot_type, axes, styles):
    """
    Adds a subplot using the data from a 'df' 'column' in the position given by its 'axes'.
    Types available: Pie, Histogram, Bar, Box.
    Optionally a 'styles' dictionary can be added in order to change the plot styles.
    """
    axes.set_title(column, fontsize=12)
    values_series = df[column].value_counts(dropna=False, normalize=True)
    if plot_type == 'Pie':
        #axes.pie(values_series.values, labels = values_series.index, autopct=autopct_generator(10))
        axes.pie(values_series.values, labels=get_new_labels(values_series.values,
                 values_series.index, styles['limit']), autopct=autopct_generator(styles['limit']))
    elif plot_type == 'Hist':
        sns.histplot(df, x=column, ax=axes, discrete=styles['discrete'])
    elif plot_type == 'Bar':
        sns.barplot(x=values_series.index, y=values_series.values, ax=axes)
    elif plot_type == 'Box':
        sns.boxplot(data=df, y=column, ax=axes)
    else:
        print("Please specify a valid plot_type: ['Pie', 'Hist', 'Bar', 'Box]")


def clean_unused_subplots(fig, axes, row, col, plot_size):
    """
    From a given a subplot 'fig' of size 'plot_size', it removes non-used 'axes' 
    starting at the given 'row', 'col' coordinates
    """
    while row < plot_size[0]:
        while col < plot_size[1]:
            fig.delaxes(axes[row, col])
            col += 1
        row += 1


def generate_subplots(df, subplot_type, n_cols=3, styles={}):
    """
    Generates an homogeneous subplot of all columns in a dataframe 'df'.
    Setting the max number of columns n_cols, the subplot is automatically arranged for 
    a better display.
    Types available: Pie, Histogram, Bar, Box.
    """
    styles = {**{'size': (40, 50), 'n_bins': 10,
                 'discrete': False, 'limit': 10}, **styles}
    # auto-scaling the subplot based on the number of columns
    n_rows = int(np.ceil([len(df.columns) / n_cols])[0])
    # setting up the subplot
    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=styles['size'], constrained_layout=True)
    fig.suptitle(styles['title'], fontsize=22)
    # plotting variables from df
    row = -1
    col = -1
    for idx, column in enumerate(df.columns):
        # managing layout
        col = (idx % n_cols)
        if col == 0:
            row += 1
        # adding subplots
        if n_rows == 1:
            add_subplot(df, column, subplot_type, axes[col], styles)
        else:
            add_subplot(df, column, subplot_type, axes[row, col], styles)
    clean_unused_subplots(fig, axes, row, col + 1, (n_rows, n_cols))
