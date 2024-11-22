import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc

from data import data_preprocessor as dp
import pandas as pd

from datetime import date

dp.load_global_df()

min_date = dp.df_global["date_created"].min().date()
max_date = dp.df_global["date_created"].max().date()

print(min_date)
print(max_date)


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.10.5/font/bootstrap-icons.min.css"
    ], suppress_callback_exceptions=True)

# Sidebar
sidebar = html.Div(
    [
        html.A(
            [
                html.Div(
                    [
                        html.Span("C", className="catch-bold", style={"color": "#39b0cd"}),
                        html.Span("at", style={"color": "#FFFFFF"}),
                        html.Span("c", style={"color": "#2677b1"}),
                        html.Span("h", style={"color": "#FFFFFF"}),
                    ],
                    className="catch-logo-text")
            ],
            href="https://catchconsulting.com.mx/",
            target="_blank",
            className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none"
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className=f"bi bi-{page.get('icon', 'info-circle')} me-2"), page["name"]],
                    href=page["path"],
                    active="exact",
                    className="text-white nav-link"
                )
                for page in dash.page_registry.values()
            ],
            vertical=True, pills=True, className="flex-column mb-auto"
        ),
    ],
    className="d-flex flex-column flex-shrink-0 p-3 text-white bg-dark sidebar"
)

# Footer
footer = html.Footer(
    html.Div(
        [
            html.Span("© 2024 Catch Consulting", className="text-body-secondary"),
            dbc.Nav(
                [
                    dbc.NavLink(
                        html.I(className="bi bi-linkedin"),
                        href="https://www.linkedin.com/company/18533142/admin/",
                        target="_blank",
                        className="text-body-secondary ms-3"
                    ),
                    dbc.NavLink(
                        html.I(className="bi bi-facebook"),
                        href="https://www.facebook.com/catch.consulting.mx",
                        target="_blank",
                        className="text-body-secondary ms-3"
                    ),
                ],
                className="d-flex justify-content-end"
            )
        ],
        className="d-flex justify-content-between align-items-center py-3 my-4 border-top"
    ),
    className="container"
)

# Layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        sidebar,
        html.Div(
            [
                html.Div([
                    html.Div([
                        html.H1("Dashboard", id="page-title"),
                        html.Div([
                            dcc.DatePickerRange(id="date-picker-range",
                                                min_date_allowed=min_date,
                                                max_date_allowed=max_date,
                                                initial_visible_month=max_date,
                                                start_date=min_date,
                                                end_date=max_date,
                                                display_format="D/M/Y",
                                                minimum_nights=0)
                        ], className="date-picker-container"),
                    ], id="title-container"),
                    html.P(id="output-date-picker-range"),
                ], id="top-container"),
                dash.page_container,  # Placeholder for page content
                footer
            ],
            className="content p-4",
            style={"width": "100%", "marginLeft": "280px"}
        ),
        dcc.Store(id="filtered-date-df")
    ],
    className="d-flex"
)


@app.callback(
        Output("page-title", "children"),
        Input("url", "pathname")
)
def update_title(pathname):
    if pathname == "/":
        page = dash.page_registry.get("pages.home", {})
    else:
        page = dash.page_registry.get("pages." + pathname.strip("/").replace("-", "_"), {})
    return page.get("h1_title", "Dashboard")


@app.callback(
        Output("output-date-picker-range", "children"),
        Output("filtered-date-df", "data"),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
)
def update_date(start_date, end_date):
    text_output = ""
    start_date_object = None
    end_date_object = None

    if start_date is not None and start_date != end_date:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%d/%b/%y')

        text_output += start_date_string + " - "

    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string =  end_date_object.strftime('%d/%b/%y')

        text_output += end_date_string

    df = dp.df_global

    true = pd.Series([True] * len(df))

    condicion1 = (
        (df["date_created"] >= pd.to_datetime(start_date_object))
        if start_date_object is not None
        else true
    )
    condicion2 = (
        (df["date_created"].dt.date <= pd.to_datetime(end_date_object).date())
        if start_date_object is not None
        else true
    )

    filtered_date_df = dp.df_global[condicion1 & condicion2]
    first_row = df.iloc[[0]]

    final_df = pd.concat([first_row, filtered_date_df])

    return text_output, final_df.to_json(date_format='iso', orient='split')


if __name__ == "__main__":
    app.run(debug=True)
