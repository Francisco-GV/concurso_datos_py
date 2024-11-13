import pandas as pd
from pandas import DataFrame
import numpy as np

def eval_last(first, last, last_column_type):
    if first is not None and last is not None:
        if last_column_type.startswith("Otro"):
            return "multiple_selection"
        else:
            return "related_questions"

    return None


def get_column_range(df: DataFrame, column_name: str, get_consecutive_related_questions: bool) -> tuple:
    result = {"multiple_selection": None, "related_questions": None}
    first = None
    last = None
    last_column_type = None

    for column in df.loc[:, column_name:].columns:
        column_type = df[column].iloc[0]
        # Si esto es verdad, la pregunta no es de multiple selección
        if column_type in ["Open-Ended Response", "Response"] or not column_type:
            range_type = eval_last(first, last, last_column_type)
            if range_type:
                result[range_type].append((first, last))
            return result
        elif not column.startswith("Unnamed"):
            range_type = eval_last(first, last, last_column_type)
            if range_type:
                result[range_type].append((first, last))

            if get_consecutive_related_questions:
                first = column
            else:
                return result
        else:
            if first is not None:
                last = column
                last_column_type = column_type

    return None


def get_advisor_feedback_1_df(df):
    result = get_column_range(df, "Por favor, seleccione el o los ejecutivos que les asesoran", True)

    first1, last1 = result["multiple_selection"]
    first2, last2 = result["related_questions"]

    df_options = df.loc[:, first1:last1]
    df_questions = df.loc[:, first2:last2]

    first1 = df_options[first1].values[0]
    last1 = df_options[last1].values[0]
    first2 = df_questions[first2].values[0]
    last2 = df_questions[last2].values[0]

    advisor_df = pd.concat([df_options, df_questions], axis=1)

    advisor_names = advisor_df.iloc[0]
    advisor_df.columns = advisor_names
    advisor_df = advisor_df.drop([0]).reset_index(drop=True).replace("", np.nan)

    return advisor_df, (first1, last1), (first2, last2)


def melt(df, columns_to_keep, columns_to_melt, new_column_name):
    df_long = pd.melt(df, id_vars=columns_to_keep, value_vars=columns_to_melt,
                      var_name=new_column_name, value_name="Present")
    df_long = df_long[df_long["Present"].notna()].drop(columns="Present")
    df_long = df_long[[new_column_name] + [col for col in df_long.columns if col != new_column_name]]

    return df_long


def get_advisor_names(advisor_df, first_range):
    names = advisor_df.loc[:, first_range[0]:first_range[1]]
    return names.columns.values.flatten().tolist()


def get_particular_advisor_perfomance_df(advisor_df, second_range, name):
    df_particular = advisor_df[advisor_df[name].str.len() > 0]
    questions = df_particular.loc[:, second_range[0]:second_range[1]]

    name_index = advisor_df[name].to_frame().columns
    df_particular = df_particular.loc[:, name_index.append(questions)]

    return df_particular

