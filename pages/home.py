import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from data.analysis import advisor_feedback as af
from data.analysis import general as g
from util import graph_creator as gc


def data_to_df(data):
    if data is None:
        raise dash.exceptions.PreventUpdate
    return pd.read_json(data, orient="split")


@callback(
        Output("home-average-score-qualitative-title", "children"),
        Output("home-average-score-value", "children"),
        Output("home-max-average-score-value", "children"),
        Output("home-max-average-score-names", "children"),
        Output("home-more-participations-count", "children"),
        Output("home-more-participations-name", "children"),
        Output("type-service-pie-chart", "figure"),
        Output("recomendation-pie-chart", "figure"),
        Output("record-number-value", "children"),
        Input("filtered-date-df", "data")
)
def update_home(filtered_date_data):
    df = data_to_df(filtered_date_data)

    advisors_df, names_range, questions_range = af.get_advisor_feedback_1_df(df)
    questions = af.get_advisor_questions(advisors_df, questions_range)
    names = af.get_advisor_names(advisors_df, names_range)
    advisors_df = af.melt(advisors_df, questions + af.extra_questions, names, "Asesores")

    participation_count = af.count_participations(advisors_df, "Asesores")
    name_max_count = participation_count.idxmax()
    quantity_max_count = participation_count.max()

    cuantitative_df = af.convert_qualitative_to_cuantitative(advisors_df, questions)
    average_score_df = af.get_average_score(cuantitative_df, questions, "Asesores", "Promedio")

    max_average_score_df = af.get_max_average_score(average_score_df, "Promedio")
    general_advisor_average_score = int(float(average_score_df['Promedio'].mean()) * 10)

    average_score_title = (
        list(af.cuantitative_values.keys())[
            list(af.cuantitative_values.values()).index(
                general_advisor_average_score // 10
            )
        ],
    )
    average_score_value = f"Puntaje: {general_advisor_average_score}/100",

    max_average_score_value = str(int(max_average_score_df["Promedio"].iloc[0] * 10)) + "%"
    max_average_score_names = [
        html.P(
            name,
            className="data-text",
        )
        for name in max_average_score_df["Asesores"].to_list()
    ]

    type_service_pie_chart = gc.create_type_service_pie_chart(df)
    recommendation_pie_chart = gc.create_recomendation_pie_chart(df)

    record_number = g.get_row_number(df) - 1 # The first row is column info

    return (
        average_score_title,
        average_score_value,
        max_average_score_value,
        max_average_score_names,
        quantity_max_count,
        name_max_count,
        type_service_pie_chart,
        recommendation_pie_chart,
        record_number
    )


dash.register_page(__name__, title="Inicio", path="/", name="Inicio", h1_title="General", icon="house")

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
                                        html.P(id="record-number-value", className="data-text-important"),
                                        html.H3(
                                            "Total de respuestas",
                                            className="data-card-title",
                                        ),
                                    ],
                                    className="data-card h-100",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        html.P(id="home-average-score-qualitative-title",
                                            className="data-text-important",
                                        ),
                                        html.P(id="home-average-score-value",
                                            className="data-text",
                                        ),
                                        html.H3(
                                            "Satisfacción general con el servicio",
                                            className="data-card-title",
                                        ),
                                    ],
                                    className="data-card h-100",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        html.P(id="home-max-average-score-value", className="data-text-important"),
                                        html.Div(id="home-max-average-score-names"),
                                        html.H3(
                                            "Mejor rendimiento",
                                            className="data-card-title",
                                        ),
                                    ],
                                    className="data-card h-100",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        html.P(id="home-more-participations-count", className="data-text-important"),
                                        html.P(id="home-more-participations-name", className="data-text"),
                                        html.H3(
                                            "Más participaciones",
                                            className="data-card-title",
                                        ),
                                    ],
                                    className="data-card h-100",
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col([dcc.Graph(id="type-service-pie-chart")]),
                        dbc.Col([dcc.Graph(id="recomendation-pie-chart")]),
                    ]
                )
            ]
        )
    ]
)
