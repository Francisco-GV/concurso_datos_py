import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc

from data import data_preprocessor

from datetime import date

data_preprocessor.load_global_df()

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.10.5/font/bootstrap-icons.min.css"
])

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
                                                min_date_allowed=date(2000, 1, 1),
                                                max_date_allowed=date.today(),
                                                initial_visible_month=date.today(),
                                                end_date=date.today(),
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
        )
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
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
)
def update_date(start_date, end_date):
    print(f"Date selected: {start_date} - {end_date}")

    text_output = ""

    if start_date is not None and start_date != end_date:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%d/%b/%y')

        text_output += start_date_string + " - "

    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string =  end_date_object.strftime('%d/%b/%y')

        text_output += end_date_string


    print(f"text output: {text_output}")

    return text_output


if __name__ == "__main__":
    app.run(debug=True)
