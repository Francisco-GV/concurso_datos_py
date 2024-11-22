import pandas as pd

def get_row_number(df):
    return len(df.index)


def count_service_type(df):
    count_df = df.loc[1:, "¿Qué tipo de servicio te brindamos?"].value_counts().reset_index()
    count_df.columns = ["Servicio", "Conteo"]

    return count_df


def get_time_info_df(df, date_column):
    time_info_df = df.copy()
    time_info_df[date_column] = pd.to_datetime(time_info_df[date_column])

    time_info_df["day_of_week"] = time_info_df[date_column].dt.day_name()
    time_info_df["hour"] = time_info_df[date_column].dt.hour
    time_info_df["minute"] = time_info_df[date_column].dt.minute

    time_info_df = time_info_df[(time_info_df["hour"] != 0) | (time_info_df["minute"] != 0)]
    time_info_df["day_of_week"] = pd.Categorical(time_info_df["day_of_week"], categories=time_info_df["day_of_week"].dt.day_name().unique(), ordered=True)

    time_info_df = time_info_df.groupby(["day_of_week", "hour"]).size().reset_index(name="count")


    return time_info_df

