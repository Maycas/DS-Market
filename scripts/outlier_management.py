import pandas as pd
import numpy as np


def outlier_limits(df, col):
    """
    For a given 'df' 'col' it provides the lower and upper limits 
    of the 1.5 interquartile range
    """
    iqr = df[col].quantile(.75) - df[col].quantile(.25)
    low = df[col].quantile(.25) - 1.5 * iqr
    high = df[col].quantile(.75) + 1.5 * iqr
    return (low, high)


def has_outliers(df, col):
    """
    Returns True if df[col] has outliers, understood as values outside the 1.5 * IQR
    """
    limits = outlier_limits(df, col)
    return len(df.loc[(df[col] < limits[0]) | (df[col] > limits[1]), col]) != 0


def remove_outliers(df, col, aggfunc):
    """
    Sets the value defined in the 'aggfunc' for all values outside
    the +- 1.5 * IQR in a given 'df[col]' 
    """
    limits = outlier_limits(df, col)
    value = df[col].apply(aggfunc)
    df.loc[(df[col] < limits[0]) | (df[col] > limits[1]), col] = value
