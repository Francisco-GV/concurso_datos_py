import pandas as pd

def load_file(path):
    global main_df
    main_df = pd.read_csv(path)
    return main_df

