import dash
from dash import html, dcc, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc

from data.analysis import advisor_feedback as af
from util import graph_creator as gc
from util import util


dash.register_page(__name__, title="Nivel de atención", name="Nivel de atención", h1_title="Análisis de nivel de atención", icon="person-vcard")


@callback(
    Output("advisors-data", "data"),
    Output("advisors-questions", "data"),
    Output("advisor-dropdown", "options"),
    Output("advisor-dropdown", "value"),
    Output("more-participations-count", "children"),
    Output("more-participations-name", "children"),
    Output("average-score-img", "src"),
    Output("average-score-qualitative-title", "children"),
    Output("average-score-value", "children"),
    Output("max-average-score-value", "children"),
    Output("max-average-score-names", "children"),
    Output("average-score-graph", "figure"),
    Output("participation-count-graph", "figure"),
    Input("filtered-date-df", "data")
)
def create_advisors_data(filtered_date_data):
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

    average_score_img = f"assets/images/emotions/{general_advisor_average_score // 10}.png"
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

    average_score_graph = gc.create_average_score_graph(average_score_df)
    participation_count_graph = gc.create_participation_count_graph(participation_count)

    return (
        advisors_df.to_json(date_format='iso', orient='split'),
        questions,
        names,
        names[0],
        quantity_max_count,
        name_max_count,
        average_score_img,
        average_score_title,
        average_score_value,
        max_average_score_value,
        max_average_score_names,
        average_score_graph,
        participation_count_graph,
    )


top = dbc.Container(
    [
        dbc.Row(
            [
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
                                            html.P(id="more-participations-count", className="data-text-important"),
                                            html.H3(
                                                "Más participaciones",
                                                className="data-card-title",
                                            ),
                                            html.P(id="more-participations-name", className="data-text",),
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
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        html.Img(id="average-score-img",
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
                                            html.P(id="average-score-qualitative-title",
                                                className="data-text-important",
                                            ),
                                            html.H3(
                                                "Satisfacción general con los asesores",
                                                className="data-card-title",
                                            ),
                                            html.P(id="average-score-value",
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
                                            html.P(id="max-average-score-value", className="data-text-important"
                                            ),
                                            html.H3(
                                                "Mejor rendimiento",
                                                className="data-card-title",
                                            ),
                                            html.Div(id="max-average-score-names"),
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
                ),
            ],
            className="g-4 align-items-stretch",  # align-items-stretch para alinear alturas
        )
    ],
    fluid=True,
)

left_filter_column = dbc.Container([
    html.Label("Selecciona un asesor"),
    dcc.Dropdown(id="advisor-dropdown", clearable=False),
    html.Hr()
])


layout = [
    top,
    dbc.Row([
        dbc.Col(dcc.Graph(id="average-score-graph")),
        dbc.Col(dcc.Graph(id="participation-count-graph"))
    ]),
    dbc.Row([
        dbc.Row(left_filter_column),
        dbc.Row(dcc.Graph(id="advisor-graph"))
    ]),
    dbc.Row([
        dbc.Row(dcc.Graph(id="advisor-suggestions-wordcloud"))
    ]),
    dcc.Store(id="advisors-data"),
    dcc.Store(id="advisors-questions")
]


@callback(
        Output("advisor-graph", "figure"),
        Output("advisor-suggestions-wordcloud", "figure"),
        State("advisors-data", "data"),
        State("advisors-questions", "data"),
        Input("advisor-dropdown", "value")
)
def update_advisor_graphs(advisors_data, questions, name):
    advisor_df = util.data_to_df(advisors_data)

    title = f"Distribución de puntuación de {name} por pregunta"
    dff = advisor_df.loc[advisor_df["Asesores"] == name]

    df_melted = dff.melt(id_vars="Asesores", value_vars=questions, var_name="Pregunta", value_name="Puntuación")
    df_melted = df_melted.dropna(subset=["Puntuación"])

    question_order_dict = {question: idx for idx, question in enumerate(questions)}

    df_counts = df_melted.groupby(["Pregunta", "Puntuación"]).size().reset_index(name="Conteo")
    df_counts["valor_cuantitativo"] = df_counts["Puntuación"].map(af.cuantitative_values)
    df_counts["porcentaje"] = df_counts.groupby("Pregunta")["Conteo"].transform(lambda x: x / x.sum() * 100)
    df_counts["pregunta_orden"] = df_counts["Pregunta"].map(question_order_dict)

    df_counts = df_counts.sort_values(by=["pregunta_orden", "valor_cuantitativo"], ascending=False)

    fig =  px.bar(df_counts, x="porcentaje", y="Pregunta", color="Puntuación", orientation="h",
                  text="Conteo", title=title)

    fig.update_traces(textposition="inside", textfont_size=16)
    fig.update_layout(
        xaxis=dict(ticksuffix="%"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            traceorder="normal",
        ),
        yaxis_title=None,
        xaxis_title=None,
        legend_title_text=None
    )

    particular_advisor_df = advisor_df[advisor_df["Asesores"] == name]
    text_list = list(particular_advisor_df["¿Existe algo que podría ayudarnos a mejorar nuestro servicio?"].dropna().values)
    text = " ".join(text_list)
    wordcloud_figure = gc.create_wordcloud_figure(text)

    return fig, wordcloud_figure



