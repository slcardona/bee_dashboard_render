import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

THEME = dbc.themes.FLATLY
load_figure_template("flatly")

app = Dash(__name__, external_stylesheets=[THEME])
server = app.server
df = pd.read_csv(
    "https://raw.githubusercontent.com/lihkir/Uninorte/main/AppliedStatisticMS/DataVisualizationRPython/Lectures/Python/PythonDataSets/intro_bees.csv"
)

df = (
    df.groupby(["State", "ANSI", "Affected by", "Year", "state_code"])[["Pct of Colonies Impacted"]]
    .mean()
    .reset_index()
)

years = sorted([int(y) for y in df["Year"].dropna().unique().tolist()])
affected_vals = sorted(df["Affected by"].dropna().unique().tolist())

CARD_STYLE = {
    "borderRadius": "14px",
    "boxShadow": "0 2px 10px rgba(0,0,0,0.08)",
    "border": "none",
}

GRAPH_HEIGHT = {"height": "380px"}

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.Div(
                [
                    html.Img(src="/assets/bee.jpg", height="40px", style={"marginRight": "12px"}),  # Logo aquí
                    html.Div(
                        [
                            html.H3("Bee Colonies Dashboard", className="mb-0 fw-bold"),
                            html.Div("US Bee Colony Impact Explorer", className="text-muted"),
                        ]
                    ),
                ],
                style={"display": "flex", "alignItems": "center"},
            )
        ],
        fluid=True,
    ),
    color="white",
    dark=False,
    className="mb-4 border-bottom",
)

controls = dbc.Card(
    dbc.CardBody(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Year Range"),
                        dcc.RangeSlider(
                            id="year_range",
                            min=min(years),
                            max=max(years),
                            value=[min(years), max(years)],
                            marks={int(y): str(y) for y in years},
                            step=1,
                            allowCross=False,
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.Label("Affected by"),
                        dcc.Dropdown(
                            id="slct_aff",
                            options=[{"label": a, "value": a} for a in affected_vals],
                            value=[affected_vals[0]],
                            multi=True,
                            clearable=False,
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Label("Template"),
                        dcc.Dropdown(
                            id="slct_template",
                            options=[
                                {"label": "plotly_white", "value": "plotly_white"},
                                {"label": "ggplot2", "value": "ggplot2"},
                                {"label": "seaborn", "value": "seaborn"},
                                {"label": "simple_white", "value": "simple_white"},
                            ],
                            value="plotly_white",
                            clearable=False,
                        ),
                    ],
                    md=3,
                ),
            ],
            className="g-3",
        )
    ),
    style=CARD_STYLE,
    className="mb-4",
)

def kpi_card(title, id_name):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small"),
                html.H3(id=id_name, className="fw-bold mb-0"),
            ]
        ),
        style=CARD_STYLE,
    )

app.layout = dbc.Container(
    [
        navbar,
        controls,
        html.Div(id="output_container", className="mb-3"),
        dbc.Row(
            [
                dbc.Col(kpi_card("Average % impacted", "kpi_avg"), md=4),
                dbc.Col(kpi_card("Maximum % impacted", "kpi_max"), md=4),
                dbc.Col(kpi_card("Number of States", "kpi_states"), md=4),
            ],
            className="mb-4 g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("USA Choropleth Map"),
                                dcc.Graph(id="my_bee_map", style={"height": "500px"}),
                            ]
                        ),
                        style=CARD_STYLE,
                    ),
                    md=12,
                )
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Top States by % Impacted"),
                                dcc.Graph(id="fig_state", style=GRAPH_HEIGHT),
                            ]
                        ),
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Comparison by Affected by"),
                                dcc.Graph(id="fig_aff", style=GRAPH_HEIGHT),
                            ]
                        ),
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
            ],
            className="mb-4 g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Time Series Comparison"),
                                dcc.Graph(id="fig_year", style=GRAPH_HEIGHT),
                            ]
                        ),
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Distribution of % Impacted"),
                                dcc.Graph(id="fig_hist", style=GRAPH_HEIGHT),
                            ]
                        ),
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
            ],
            className="mb-4 g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Boxplot by Cause"),
                                dcc.Graph(id="fig_box", style={"height": "420px"}),
                            ]
                        ),
                        style=CARD_STYLE,
                    ),
                    md=12,
                )
            ]
        ),
    ],
    fluid=True,
    style={"backgroundColor": "#F8F9FA", "padding": "25px"},
)

@app.callback(
    Output("output_container", "children"),
    Output("kpi_avg", "children"),
    Output("kpi_max", "children"),
    Output("kpi_states", "children"),
    Output("my_bee_map", "figure"),
    Output("fig_state", "figure"),
    Output("fig_aff", "figure"),
    Output("fig_year", "figure"),
    Output("fig_hist", "figure"),
    Output("fig_box", "figure"),
    Input("year_range", "value"),
    Input("slct_aff", "value"),
    Input("slct_template", "value"),
)
def update_graph(year_range, affected_by, template):
    start_year, end_year = year_range

    if not isinstance(affected_by, list):
        affected_by = [affected_by]

    dff = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)].copy()
    map_df = dff[dff["Affected by"].isin(affected_by)].copy()

    title = html.H6(
        f"Years: {start_year}–{end_year} | Causes: {', '.join(affected_by)}"
    )

    if map_df.empty:
        empty_fig = px.scatter(template=template)
        empty_fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[{
                "text": "No data for selected filters",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 18}
            }]
        )
        return (
            title,
            "0%",
            "0%",
            "0",
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
        )

    avg_val = round(map_df["Pct of Colonies Impacted"].mean(), 2)
    max_val = round(map_df["Pct of Colonies Impacted"].max(), 2)
    n_states = map_df["State"].nunique()

    fig_map = px.choropleth(
        map_df,
        locationmode="USA-states",
        locations="state_code",
        scope="usa",
        color="Pct of Colonies Impacted",
        hover_data=["State", "Affected by", "Year"],
        color_continuous_scale="YlOrRd",
        template=template,
    )

    g_state = (
        map_df.groupby("State", as_index=False)["Pct of Colonies Impacted"]
        .mean()
        .sort_values("Pct of Colonies Impacted", ascending=False)
        .head(10)
    )

    fig_state = px.bar(
        g_state,
        x="Pct of Colonies Impacted",
        y="State",
        orientation="h",
        template=template,
        text_auto=".1f",
    )
    fig_state.update_layout(yaxis={"categoryorder": "total ascending"})

    g_aff = (
        dff.groupby("Affected by", as_index=False)["Pct of Colonies Impacted"]
        .mean()
        .sort_values("Pct of Colonies Impacted", ascending=False)
    )

    fig_aff = px.bar(
        g_aff,
        x="Affected by",
        y="Pct of Colonies Impacted",
        template=template,
        text_auto=".1f",
    )
    fig_aff.update_layout(xaxis_tickangle=-20)

    ts = (
        dff[dff["Affected by"].isin(affected_by)]
        .groupby(["Year", "Affected by"], as_index=False)["Pct of Colonies Impacted"]
        .mean()
        .sort_values(["Affected by", "Year"])
    )

    fig_year = px.line(
        ts,
        x="Year",
        y="Pct of Colonies Impacted",
        color="Affected by",
        markers=True,
        template=template,
    )

    fig_hist = px.histogram(
        map_df,
        x="Pct of Colonies Impacted",
        nbins=15,
        template=template,
    )

    fig_box = px.box(
        map_df,
        x="Affected by",
        y="Pct of Colonies Impacted",
        template=template,
        points="outliers",
    )
    fig_box.update_layout(xaxis_tickangle=-20)

    return (
        title,
        f"{avg_val}%",
        f"{max_val}%",
        f"{n_states}",
        fig_map,
        fig_state,
        fig_aff,
        fig_year,
        fig_hist,
        fig_box,
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)