import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

from datetime import date
from data.analysis import advisor_feedback as af
from data.analysis import historical_analysis as ha
from util import graph_creator as gc
from util import util

dash.register_page(__name__, title="Análisis Histórico", name="Análisis Histórico", h1_title="Análisis Histórico", icon="clock-history")


@callback(
    Output("general-average-score-period", "figure"),
    Output("service-trend-period-graph", "figure"),
    Output("advisor-participation-period-graph", "figure"),
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
    names = af.get_advisor_names(advisors_df, names_range)
    cuantitative_df = af.convert_qualitative_to_cuantitative(advisors_df, questions)
    advisors_df = af.melt(advisors_df, questions + af.extra_questions + af.info, names, "Asesores")

    services_column_name = "¿Qué tipo de servicio te brindamos?"
    average_df = ha.determine_general_average_score_on_period(
        cuantitative_df, "date_created", start_date, end_date, questions
    )
    service_trend_df = ha.determine_service_trend_on_period(
        df.iloc[1:], "date_created", services_column_name, start_date, end_date
    )
    participation_df = ha.determine_advisor_participation_on_period(
        advisors_df, "date_created", start_date, end_date
    )

    return (
        gc.create_average_score_period_graph(average_df, questions),
        gc.create_service_trend_period_graph(service_trend_df, services_column_name),
        gc.create_advisor_participation_period_graph(participation_df),
    )


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
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dcc.Graph(id="service-trend-period-graph")
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dcc.Graph(id="advisor-participation-period-graph")
                                    ]
                                )
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)
