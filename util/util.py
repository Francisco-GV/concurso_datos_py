import dash
import pandas as pd
import io

def data_to_df(data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    return pd.read_json(io.StringIO(data), orient="split")