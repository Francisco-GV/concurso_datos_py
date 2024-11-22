import os
import pandas as pd

individual_columns_to_delete = [
    "collector_id",
    "Correo Electrónico",
    "Teléfono",
]

range_columns_to_delete = [
    ("ip_address", "custom_1"),
    ("¿Qué tipo de servicio te brindamos? ", "Comparte como fue tu experiencia con tu ejecutivo de cuenta en la implementación del servicio."),
]

csv_path = os.path.join("resources", "Satisfacción de servicio para UPG 2024.csv")
df_global = None

def load_file(path):
    main_df = pd.read_csv(path)
    return main_df

def load_global_df():
    global df_global
    df_global = load_file(csv_path)

    preprocess_global_df()


def preprocess_global_df():
    global df_global
    # Convierte las columnas de fecha en tipo datetime para realizar operaciones con fechas
    df_global["date_created"] = pd.to_datetime(df_global["date_created"], format="mixed")
    df_global["date_modified"] = pd.to_datetime(df_global["date_modified"], format="mixed")

    columns_to_delete = individual_columns_to_delete.copy()

    for start_col, end_col in range_columns_to_delete:
        cols_in_range = df_global.loc[:, start_col:end_col].columns.tolist()
        columns_to_delete.extend(cols_in_range)

    # Elimina columnas que no se ocupan
    df_global = df_global.drop(columns=columns_to_delete)

