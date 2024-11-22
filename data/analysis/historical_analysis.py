import pandas as pd
from pandas import DataFrame
import numpy as np
import difflib


def determine_grouping_level(start_date, end_date):
    delta = (end_date - start_date).days

    if delta <= 31:
        grouping_level = "D"
    elif delta <= 760:
        grouping_level = "M"
    else:
        grouping_level = "Y"

    return grouping_level



def determine_general_average_score_on_period(df, date_column, start_date, end_date, questions):
    grouping_level = determine_grouping_level(start_date, end_date)

    df[date_column] = pd.to_datetime(df[date_column])

    df["period"] = df[date_column].dt.to_period(freq = grouping_level)

    average = df.groupby("period")[questions].mean().reset_index()

    average[questions] = average[questions].interpolate(method='linear', limit_direction='both')

    average["period"] = average["period"].dt.strftime({
            'D': '%d/%m/%Y',
            'M': '%m/%Y',
            'Y': '%Y'
    }[grouping_level])

    for question in questions:
        average[question] = pd.to_numeric(average[question], errors='coerce')

    return average

