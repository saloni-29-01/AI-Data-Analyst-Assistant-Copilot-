import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

engine = create_engine("duckdb:///analytics.duckdb")

def generate_chart():
    query = """
    SELECT users.name, SUM(sales.amount) as revenue
    FROM sales
    JOIN users ON sales.user_id = users.user_id
    GROUP BY users.name
    ORDER BY revenue DESC
    LIMIT 5
    """

    df = pd.read_sql(query, engine)

    fig = px.bar(df, x="name", y="revenue", title="Top Customers Revenue")

    return fig