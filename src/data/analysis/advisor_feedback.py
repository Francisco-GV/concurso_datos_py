from pandas import DataFrame

def eval_last(first, last, last_column_type) -> bool:
    if first is not None and last is not None:
        if last_column_type.startswith("Otro"):
            return True
    return False


def get_column_range(df: DataFrame, column_name) -> DataFrame:
    first = None
    last = None
    last_column_type = None

    for column in df.loc[:, column_name:].columns:
        column_type = df[column].iloc[0]
        # Si esto es verdad, la pregunta no es de multiple selección
        if column_type in ["Open-Ended Response", "Response"] or not column_type:
            return None


        if not column.startswith("Unnamed"):
            if first is not None:
                if eval_last(first, last, last_column_type):
                    return df.loc[:, first:last]
                else:
                    return None
            else:
                first = column
        else:
            if first is not None:
                last = column
                last_column_type = column_type

    return None
