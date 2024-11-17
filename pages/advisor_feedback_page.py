import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

from data.analysis import advisor_feedback as af
from data import data_preprocessor as dp

df = dp.df_global

advisor_df, names_range, questions_range = af.get_advisor_feedback_1_df(df)

questions = af.get_advisor_questions(advisor_df, questions_range)
names = af.get_advisor_names(advisor_df, names_range)
advisor_df = af.melt(advisor_df, questions, names, "Asesores")

participation_count = af.count_participations(advisor_df, "Asesores")

name_max_count = participation_count.idxmax()
quantity_max_count = participation_count.max()

dash.register_page(__name__, title="Asesores", name="Asesores", h1_title="Retroalimentación de Asesores", icon="person-vcard")

top = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.P("200", className="data-text-important"),
                            html.H3(
                                "Número total de registros", className="data-card-title"
                            ),
                        ],
                        className="data-card h-100 d-flex flex-column justify-content-center align-items-center",  # h-100 asegura que todas las tarjetas tengan igual altura
                    ),
                    xs=12,
                    sm=6,
                    md=4,
                    lg=3
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        html.Img(
                                            src="assets/images/avatar/default_avatar.png",
                                            alt="avatar",
                                            className="rounded-circle img-fluid",
                                        ),
                                        className="avatar-container",
                                    ),
                                    width="auto",
                                    className="d-flex align-items-center justify-content-center",
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.P(
                                                quantity_max_count, className="data-text-important"
                                            ),
                                            html.H3(
                                                "Más participaciones",
                                                className="data-card-title",
                                            ),
                                            html.P(
                                                name_max_count,
                                                className="data-text",
                                            ),
                                        ],
                                        className="info-container",
                                    ),
                                    width=True,
                                ),
                            ],
                            className="g-0",
                        ),
                        className="data-card data-card-horizontal h-100",
                    ),
                    xs=12,
                    sm=6,
                    md=4,
                    lg=3
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        html.Img(
                                            src="assets/images/emotions/feliz.png",
                                            alt="emotion",
                                            className="img-fluid",
                                        ),
                                        className="icon-container",
                                    ),
                                    width="auto",
                                    className="d-flex align-items-center justify-content-center",
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.P(
                                                "Bueno", className="data-text-important"
                                            ),
                                            html.H3(
                                                "Satisfacción general con los asesores",
                                                className="data-card-title",
                                            ),
                                            html.P(
                                                "Puntaje: 80/100", className="data-text"
                                            ),
                                        ],
                                        className="info-container",
                                    ),
                                    width=True,
                                ),
                            ],
                            className="g-0",
                        ),
                        className="data-card data-card-horizontal h-100",
                    ),
                    xs=12,
                    sm=6,
                    md=4,
                    lg=3
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        html.Img(
                                            src="assets/images/avatar/default_avatar.png",
                                            alt="avatar",
                                            className="rounded-circle img-fluid",
                                        ),
                                        className="avatar-container",
                                    ),
                                    width="auto",
                                    className="d-flex align-items-center justify-content-center",
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.P(
                                                "80%", className="data-text-important"
                                            ),
                                            html.H3(
                                                "Mejor rendimiento",
                                                className="data-card-title",
                                            ),
                                            html.P(
                                                "Nombre de ejecutivo",
                                                className="data-text",
                                            ),
                                        ],
                                        className="info-container",
                                    ),
                                    width=True,
                                ),
                            ],
                            className="g-0",
                        ),
                        className="data-card data-card-horizontal h-100",
                    ),
                    xs=12,
                    sm=6,
                    md=4,
                    lg=3
                ),
            ],
            className="g-4 align-items-stretch",  # align-items-stretch para alinear alturas
        )
    ],
    fluid=True,
)

layout = [
    top,
    dcc.Dropdown(questions, questions[0], id="dropdown-questions"),
    dcc.Dropdown(names, names[0], id="dropdown-names"),
    dcc.Graph(id="graph-content")
]

@callback(
    Output("graph-content", "figure"),
    [Input("dropdown-questions", "value"), Input("dropdown-names", "value")]
)
def update_graph(question, name):
    count_column_name = "Conteo"

    dff = advisor_df.loc[advisor_df.Asesores==name, ["Asesores", question]]
    dff = af.count_qualitative_responses(dff, "Asesores", question, count_column_name)
    return px.bar(dff, x=question, y=count_column_name)
