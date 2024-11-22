import dash
import pandas as pd
import io

def data_to_df(data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    return pd.read_json(io.StringIO(data), orient="split")


def insert_line_breaks(text, max_length, line_break_char):
    words = text.split()
    result = ""
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 > max_length:
            result += line_break_char + word
            current_length = len(word)
        elif result:
            result += " " + word
            current_length += len(word) + 1
        else:
            result = word
            current_length = len(word)

    return result


