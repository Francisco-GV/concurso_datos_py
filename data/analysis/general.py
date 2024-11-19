def get_row_number(df):
    return len(df.index)


def count_service_type(df):
    count_df = df.loc[1:, "¿Qué tipo de servicio te brindamos?"].value_counts().reset_index()
    count_df.columns = ["Servicio", "Conteo"]

    return count_df

