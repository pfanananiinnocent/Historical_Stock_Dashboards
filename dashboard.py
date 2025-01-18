import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load data
companies = ["MSFT", "AAPL", "NFLX", "META", "AMZN"] 
data = {}

for company in companies:
    try:
        # Load CSV data for each company
        data[company] = pd.read_csv(f"{company}_data.csv", index_col=0, parse_dates=True)
    except FileNotFoundError:
        print(f"Data for {company} not found. Ensure fetch_data.py was run.")

# Initialize the Dash app
app = dash.Dash(__name__)

# dashboard layout
app.layout = html.Div([
    html.H1("Historical Stock Prices Dashboard", style={"textAlign": "center"}),

    # Dropdown to select a company
    dcc.Dropdown(
        id="company-dropdown",
        options=[{"label": company, "value": company} for company in companies],
        value="MSFT",  # Default company
    ),

    # Graph to display stock data
    dcc.Graph(id="stock-graph"),
])

#update the graph based on dropdown selection
@app.callback(
    Output("stock-graph", "figure"),
    [Input("company-dropdown", "value")]
)
def update_graph(selected_company):
    # Get the data for the selected company
    df = data[selected_company]

    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price"
    ))
    figure.update_layout(
        title=f"{selected_company} Stock Prices",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white"
    )
    return figure
#app
if __name__ == "__main__":
    app.run_server(debug=True)
