import pandas as pd
from pandas import DataFrame
import numpy as np


cuantitative_values = {
    "Pésimo": 3,
    "Muy Malo": 4,
    "Malo": 5,
    "Regular - Malo": 6,
    "Regular - Bueno": 7,
    "Bueno": 8,
    "Muy Bueno": 9,
    "Excelente": 10
}


extra_questions = [
    "¿Contratarías nuevamente nuestros servicios?",
    "¿Recomendarías nuestros servicios?",
    "¿Existe algo que podría ayudarnos a mejorar nuestro servicio?"
]


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
                result[range_type] = (first, last)
            return result
        elif not column.startswith("Unnamed"):
            range_type = eval_last(first, last, last_column_type)
            if range_type:
                result[range_type] = (first, last)

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
    advisor_df = advisor_df.drop([0])

    extra_questions_df = df.loc[1:, extra_questions]
    advisor_df = pd.concat([advisor_df, extra_questions_df], axis=1)

    advisor_df = advisor_df.reset_index(drop=True).replace("", np.nan)

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

def get_advisor_questions(advisor_df, second_range):
    questions = advisor_df.loc[:, second_range[0]:second_range[1]]
    return questions.columns.values.flatten().tolist()


def get_particular_advisor_perfomance_df(advisor_df, second_range, name):
    df_particular = advisor_df[advisor_df[name].str.len() > 0]
    questions = df_particular.loc[:, second_range[0]:second_range[1]]

    name_index = advisor_df[name].to_frame().columns
    df_particular = df_particular.loc[:, name_index.append(questions)]

    return df_particular


def count_qualitative_responses(particular_advisor_df, group_column_name, question, count_column_name):
    count_df = (particular_advisor_df
                .groupby(group_column_name)[question]
                .value_counts()
                .reset_index(name=count_column_name))
    return count_df


def count_participations(df_long, key_column_name):
    return df_long[key_column_name].value_counts()


def convert_qualitative_to_cuantitative(df_long, columns):
    df_copy = df_long.copy()
    df_copy[columns] = df_copy[columns].map(cuantitative_values.get)
    return df_copy


def get_average_score(cuantitative_df, columns, key_column_name, average_column_name):
    cuantitative_df[average_column_name] = cuantitative_df.loc[:, columns].mean(axis=1)
    average_score_df = cuantitative_df.groupby(key_column_name)[average_column_name].mean().reset_index()

    return average_score_df


def get_max_average_score(average_score_df, column_name):
    max_average = average_score_df[column_name].max()
    max_average_df = average_score_df.loc[average_score_df[column_name] == max_average]
    return max_average_df

