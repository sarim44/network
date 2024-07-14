import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import sqlite3

def load_asset_data():
    conn = sqlite3.connect('it_assets.db')
    df = pd.read_sql_query('SELECT * FROM assets', conn)
    conn.close()
    return df

def load_network_data():
    return pd.read_csv('network_data.csv')

def create_dashboard(asset_df, network_df):
    asset_fig = px.bar(asset_df, x='name', y='usage_hours', title='Asset Usage Hours')
    network_fig = px.scatter(network_df, x='packet_drops', y='latency', color='failure', title='Network Performance')

    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.H1(children='IT Management Dashboard'),
        dcc.Graph(id='asset-graph', figure=asset_fig),
        dcc.Graph(id='network-graph', figure=network_fig)
    ])
    return app

def main():
    asset_df = load_asset_data()
    network_df = load_network_data()
    app = create_dashboard(asset_df, network_df)
    app.run_server(debug=True)

if __name__ == "__main__":
    main()
