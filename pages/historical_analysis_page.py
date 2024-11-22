import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

from datetime import date
from data.analysis import advisor_feedback as af
from data.analysis import historical_analysis as ha
from util.graph_creator import create_average_score_period_graph
from util import util

dash.register_page(__name__, title="Análisis Histórico", name="Análisis Histórico", h1_title="Análisis Histórico", icon="clock-history")


@callback(
    Output("general-average-score-period", "figure"),
    Input("filtered-date-df", "data"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
)
def update_historial_analysis(filtered_date_data, start_date, end_date):
    df = util.data_to_df(filtered_date_data)

    start_date = pd.to_datetime(date.fromisoformat(start_date))
    end_date = pd.to_datetime(date.fromisoformat(end_date))

    advisors_df, names_range, questions_range = af.get_advisor_feedback_1_df(df)
    questions = af.get_advisor_questions(advisors_df, questions_range)
    cuantitative_df = af.convert_qualitative_to_cuantitative(advisors_df, questions)

    average_df = ha.determine_general_average_score_on_period(cuantitative_df, "date_created", start_date, end_date, questions)

    return create_average_score_period_graph(average_df, questions)


layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dcc.Graph(id="general-average-score-period")
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)