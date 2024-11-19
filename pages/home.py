import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from data.analysis import advisor_feedback as af
from data.analysis import general as g
from data import data_preprocessor as dp

df = dp.df_global

advisor_df, names_range, questions_range = af.get_advisor_feedback_1_df(df)

questions = af.get_advisor_questions(advisor_df, questions_range)
names = af.get_advisor_names(advisor_df, names_range)
advisor_df = af.melt(advisor_df, questions + af.extra_questions, names, "Asesores")

participation_count = af.count_participations(advisor_df, "Asesores")

name_max_count = participation_count.idxmax()
quantity_max_count = participation_count.max()

cuantitative_df = af.convert_qualitative_to_cuantitative(advisor_df, questions)
average_score_df = af.get_average_score(cuantitative_df, questions, "Asesores", "Promedio")
max_average_score_df = af.get_max_average_score(average_score_df, "Promedio")
general_advisor_average_score = int(float(average_score_df['Promedio'].mean()) * 10)


record_number = g.get_row_number(df) - 1 # The first row is column info

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
                                        html.P(record_number, className="data-text-important"),
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
                                        html.P(
                                            list(af.cuantitative_values.keys())[
                                                list(af.cuantitative_values.values()).index(
                                                    general_advisor_average_score // 10
                                                )
                                            ],
                                            className="data-text-important",
                                        ),
                                        html.P(
                                            f"Puntaje: {general_advisor_average_score}/100",
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
                                        html.P(
                                            str(int(max_average_score_df["Promedio"].iloc[0] * 10)) + "%", className="data-text-important"
                                        ),
                                        html.Div([
                                            html.P(
                                                name,
                                                className="data-text",
                                            )
                                            for name in max_average_score_df["Asesores"].to_list()
                                        ]),
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
                                        html.P(
                                            quantity_max_count, className="data-text-important"
                                        ),
                                        html.P(
                                            name_max_count,
                                            className="data-text",
                                        ),
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
                )
            ]
        )
    ]
)
