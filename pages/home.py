import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from data.analysis import advisor_feedback as af
from data.analysis import general as g
from util import graph_creator as gc
from util import util


share_authorization_column = "Para finalizar, nos encantaría poder presentarlos como uno más de nuestros clientes;" \
    " ¿nos autorizan poder usar el nombre comercial como parte de nuestra cartera de clientes?Esto solo es por fines" \
    " de referencia de nuestros servicios. Nos comprometemos a siempre guardar la confidencialidad de la información" \
    " de nuestros clientes y asociados comerciales.Si tienes alguna duda, por favor pueden consultar nuestro aviso de" \
    " confidencialidad.www.catch.com.mx/aviso_de_privacidad_consulting"


@callback(
        Output("home-average-score-qualitative-title", "children"),
        Output("home-average-score-value", "children"),
        Output("home-max-average-score-value", "children"),
        Output("home-max-average-score-names", "children"),
        Output("home-more-participations-count", "children"),
        Output("home-more-participations-name", "children"),
        Output("type-service-pie-chart", "figure"),
        Output("recomendation-pie-chart", "figure"),
        Output("recontract-pie-chart", "figure"),
        Output("share-authorization-pie-chart", "figure"),
        Output("record-number-value", "children"),
        Input("filtered-date-df", "data")
)
def update_home(filtered_date_data):
    df = util.data_to_df(filtered_date_data)

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

    type_service_pie_chart = gc.create_type_service_pie_chart(df.iloc[1:])
    recommendation_pie_chart = gc.create_recomendation_pie_chart(df.iloc[1:])
    recontract_pie_chart = gc.create_recontract_pie_chart(df.iloc[1:])
    share_authorization_pie_chart = gc.create_share_authorization_chart(df.iloc[1:], share_authorization_column)

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
        share_authorization_pie_chart,
        recontract_pie_chart,
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
                        dbc.Col([dcc.Graph(id="recontract-pie-chart")]),
                        dbc.Col([dcc.Graph(id="share-authorization-pie-chart")]),
                    ]
                )
            ]
        )
    ]
)
