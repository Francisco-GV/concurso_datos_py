
import plotly.express as px
from data.analysis import general as g
from data.analysis import advisor_feedback as af


def insert_line_breaks(text, max_length, line_break_char):
    words = text.split()
    result = ""
    current_length = 0
    for word in words:
        if current_length + len(word) + 1 > max_length:
            result += line_break_char + word
            current_length = len(word)
        elif result:
            result += " " + word
            current_length += len(word) + 1
        else:
            result = word
            current_length = len(word)

    return result


def create_average_score_graph(average_score_df):
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


def create_participation_count_graph(participation_count):
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


def create_question_pie_chart(advisor_df, title, question):
    count_df = advisor_df[question].value_counts().reset_index()
    count_df.columns = ["Respuesta", "Conteo"]

    fig = px.pie(count_df, values="Conteo", names="Respuesta", title=title)

    return fig


def create_type_service_pie_chart(df):
    title = "Servicios brindados"
    count_df = g.count_service_type(df)
    count_df['Servicio'] = count_df['Servicio'].apply(lambda x: insert_line_breaks(x, 20, "<br>"))
    fig = px.pie(count_df, values="Conteo", names="Servicio", title=title)

    return fig


def create_recomendation_pie_chart(advisor_df):
    title = "Clientes que recomendarían el servicio"
    count_df = advisor_df[af.extra_questions[0]].value_counts().reset_index()
    count_df.columns = ["Respuesta", "Conteo"]

    fig = px.pie(count_df, values="Conteo", names="Respuesta", title=title)

    return fig

