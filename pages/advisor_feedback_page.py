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

cuantitative_df = af.convert_qualitative_to_cuantitative(advisor_df, questions)
average_score_df = af.get_average_score(cuantitative_df, questions, "Asesores", "Promedio")
max_average_score_df = af.get_max_average_score(average_score_df, "Promedio")

dash.register_page(__name__, title="Asesores", name="Asesores", h1_title="Retroalimentación de Asesores", icon="person-vcard")

general_advisor_average_score = int(float(average_score_df['Promedio'].mean()) * 10)

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
                                            src=f"assets/images/emotions/{general_advisor_average_score // 10}.png",
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
                                                list(af.cuantitative_values.keys())[
                                                    list(af.cuantitative_values.values()).index(
                                                        general_advisor_average_score // 10
                                                    )
                                                ],
                                                className="data-text-important",
                                            ),
                                            html.H3(
                                                "Satisfacción general con los asesores",
                                                className="data-card-title",
                                            ),
                                            html.P(
                                                f"Puntaje: {general_advisor_average_score}/100",
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
                                                str(int(max_average_score_df["Promedio"].iloc[0] * 10)) + "%", className="data-text-important"
                                            ),
                                            html.H3(
                                                "Mejor rendimiento",
                                                className="data-card-title",
                                            ),
                                            html.Div([
                                                html.P(
                                                    name,
                                                    className="data-text",
                                                )
                                                for name in max_average_score_df["Asesores"].to_list()
                                            ]),
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


def create_average_score_graph():
    fig = px.bar(average_score_df.sort_values(by=["Promedio"], ascending=False), x="Asesores", y="Promedio")

    min = average_score_df["Promedio"].min()
    min = min - 1 if min - 1 >= 0 else 0

    fig.update_layout(yaxis=dict(range=[min, 10]))
    return fig


def create_participation_count_graph():
    sorted_series = participation_count.sort_values(ascending=False)
    fig = px.bar(sorted_series, x=sorted_series.index, y=sorted_series.values)

    max_participation = participation_count.max()
    min_participation = participation_count.min()

    min = min_participation - 1 if min_participation - 1 >= 0 else 0

    fig.update_layout(yaxis=dict(range=[min, max_participation]))
    return fig


layout = [
    top,
    dbc.Row([
        dbc.Col(dcc.Graph(figure=create_average_score_graph())),
        dbc.Col(dcc.Graph(figure=create_participation_count_graph()))
    ]),
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
