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
