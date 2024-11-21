import os
import pandas as pd

csv_path = os.path.join("test", "Satisfacción de servicio para UPG 2024.csv")
df_global = None

def load_file(path):
    main_df = pd.read_csv(path)
    return main_df

def load_global_df():
    global df_global
    df_global = load_file(csv_path)

    preprocess_global_df()


def preprocess_global_df():
    # Convierte las columnas de fecha en tipo datetime para realizar operaciones con fechas
    df_global["date_created"] = pd.to_datetime(df_global["date_created"], format="mixed")
    df_global["date_modified"] = pd.to_datetime(df_global["date_modified"], format="mixed")

