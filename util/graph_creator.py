import plotly.express as px
from data.analysis import general as g
from data.analysis import advisor_feedback as af
from wordcloud import WordCloud
import nltk
import plotly.graph_objs as go
from util import util
import pandas as pd


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
    count_df['Servicio'] = count_df['Servicio'].apply(lambda x: util.insert_line_breaks(x, 20, "<br>"))
    fig = px.pie(count_df, values="Conteo", names="Servicio", title=title)

    return fig


def create_recomendation_pie_chart(advisor_df):
    title = "Clientes que recomendarían el servicio"
    count_df = advisor_df[af.extra_questions[0]].value_counts().reset_index()
    count_df.columns = ["Respuesta", "Conteo"]

    fig = px.pie(count_df, values="Conteo", names="Respuesta", title=title)

    return fig


def create_recontract_pie_chart(advisor_df):
    title = "Clientes que volverían a contratar el servicio"
    count_df = advisor_df[af.extra_questions[1]].value_counts().reset_index()
    count_df.columns = ["Respuesta", "Conteo"]

    fig = px.pie(count_df, values="Conteo", names="Respuesta", title=title)

    return fig


def create_share_authorization_chart(df, column):
    title = "Clientes que autorizaron ser nombrados"
    count_df = df[column].value_counts().reset_index()
    count_df.columns = ["Respuesta", "Conteo"]
    count_df['Respuesta'] = count_df['Respuesta'].apply(lambda x: util.insert_line_breaks(x, 20, "<br>"))

    fig = px.pie(count_df, values="Conteo", names="Respuesta", title=title)

    return fig


def create_average_score_period_graph(average_df, questions):
    title = "Promedio de satisfacción con el servicio"

    fig = px.line(
        average_df,
        x="period",
        y=questions,
        markers=True,
        title=title,
        labels={"value": "Promedio"})

    fig.update_layout(xaxis_title=None)

    return fig


def create_service_trend_period_graph(trend_df, services_column_name):
    title = "Tendencia de contratación de servicios"

    trend_df[services_column_name] = trend_df[services_column_name].apply(
        lambda x: util.insert_line_breaks(x, 30, "<br>")
    )

    fig = px.line(
        trend_df,
        x="period_timestamp",
        y="Conteo",
        markers=True,
        color=services_column_name,
        title=title,
        labels={"Conteo": "Cantidad"}
    )

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=trend_df["period_timestamp"],
            ticktext=trend_df["period_formatted"]
        ),
        legend=dict(
            title="Servicios"
        ),
    )

    fig.update_layout(xaxis_title=None)

    return fig


def create_advisor_participation_period_graph(participation_df):
    title = "Participación de asesor a lo largo del tiempo"

    fig = px.line(
        participation_df,
        x="period_timestamp",
        y="Conteo",
        color="Asesores",
        markers=True,
        title=title,
        labels={"Conteo": "Participaciones"}
    )

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=participation_df["period_timestamp"],
            ticktext=participation_df["period_formatted"]
        ),
        legend=dict(
            title="Asesores"
        ),
    )

    fig.update_layout(xaxis_title=None)

    return fig


def create_datetime_heatmap(datetime_df):
    fig = px.density_heatmap(
        datetime_df,
        x="hour",
        y="day_of_week",
        z="count",
        color_continuous_scale="Viridis",
        labels={"hour": "Hora", "day_of_week": "Día", "count": "Frecuencia"},
        title="Frecuencia de encuestas por día y hora"
    )

    return fig


def create_wordcloud_figure(text):
    if len(text) == 0:
        return {}

    wordcloud = WordCloud(stopwords=set(nltk.corpus.stopwords.words('spanish')), max_words=100, max_font_size=90)
    wordcloud.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in wordcloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x_arr = []
    y_arr = []
    for i in position_list:
        x_arr.append(i[0])
        y_arr.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 80)

    trace = go.Scatter(
        x=x_arr,
        y=y_arr,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,
    )

    layout = go.Layout(
        {
            "xaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 250],
            },
            "yaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 450],
            },
            "margin": dict(t=50, b=20, l=10, r=10, pad=4),
            "hovermode": "closest",
            "title": "Frecuencia de palabras en sugerencias de clientes",
        }
    )

    wordcloud_figure_data = {"data": [trace], "layout": layout}

    return wordcloud_figure_data
