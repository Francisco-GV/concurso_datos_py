import pandas as pd 
from pandas import DataFrame

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

    advisor_df = pd.concat([df_options, df_questions], axis=1)

    return advisor_df
