import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from data.analysis import advisor_feedback as af
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

dash.register_page(__name__, title="Nivel de atención", name="Nivel de atención", h1_title="Análisis de nivel de atención", icon="person-vcard")

general_advisor_average_score = int(float(average_score_df['Promedio'].mean()) * 10)

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
                ),
            ],
            className="g-4 align-items-stretch",  # align-items-stretch para alinear alturas
        )
    ],
    fluid=True,
)

left_filter_column = dbc.Container([
    html.Label("Selecciona un asesor"),
    dcc.Dropdown(names, names[0], id="advisor-dropdown", clearable=False),
    html.Hr()
])

def create_average_score_graph():
    title = "Promedio de satisfacción por asesor"
    fig = px.bar(
        average_score_df.sort_values(by=["Promedio"], ascending=False),
        x="Asesores",
        y="Promedio",
        title=title,
    )

    min = average_score_df["Promedio"].min()
    min = min - 1 if min - 1 >= 0 else 0

    fig.update_layout(yaxis=dict(range=[min, 10]))
    return fig


def create_participation_count_graph():
    title = "Conteo de participación por asesor"
    sorted_series = participation_count.sort_values(ascending=False)
    fig = px.bar(
        sorted_series,
        x=sorted_series.index,
        y=sorted_series.values,
        title=title
    )

    max_participation = participation_count.max()
    min_participation = participation_count.min()

    min = min_participation - 1 if min_participation - 1 >= 0 else 0

    fig.update_layout(yaxis=dict(range=[min, max_participation]))
    return fig


def create_question_pie_chart(title, question):
    count_df = advisor_df[question].value_counts().reset_index()
    count_df.columns = ["Respuesta", "Conteo"]

    fig = px.pie(count_df, values="Conteo", names="Respuesta", title=title)

    return fig


layout = [
    top,
    dbc.Row([
        dbc.Col(dcc.Graph(figure=create_question_pie_chart("Porcentaje de clientes que contratarían nuevamente el servicio", af.extra_questions[0]))),
        dbc.Col(dcc.Graph(figure=create_question_pie_chart("Porcentaje de clientes que recomendarían el servicio", af.extra_questions[1]))),
        dbc.Col(dcc.Graph(figure=create_average_score_graph())),
        dbc.Col(dcc.Graph(figure=create_participation_count_graph()))
    ]),
    dbc.Row([
        dbc.Row(left_filter_column),
        dbc.Row(dcc.Graph(id="advisor-graph"))
    ]),
]


@callback(
        Output("advisor-graph", "figure"),
        Input("advisor-dropdown", "value")
)
def update_advisor_graph(name):
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

    return fig
