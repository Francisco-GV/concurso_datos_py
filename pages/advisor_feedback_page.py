import dash
from dash import html, dcc, callback, Output, Input
import plotly.express as px

from data.analysis import advisor_feedback as af
from data import data_preprocessor as dp

csv_path = "C:\\Dev\\ConcursoDatos\\test\\Satisfacción de servicio para UPG 2024.csv"
df = dp.load_file(csv_path)
advisor_df, names_range, questions_range = af.get_advisor_feedback_1_df(df)

questions = af.get_advisor_questions(advisor_df, questions_range)
names = af.get_advisor_names(advisor_df, names_range)

advisor_df = af.melt(advisor_df, questions, names, "Asesores")

dash.register_page(__name__, name="Asesores", icon="person-vcard")

layout = [
    html.H1(children="Asesores", style={"textAlign":"center"}),
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

