import streamlit as st
import sqlite3
import pandas as pd

st.title("AI Data Analyst Assistant")

conn = sqlite3.connect("sales.db")

# Customers Data
st.subheader("Customers Data")
df = pd.read_sql_query("SELECT * FROM customers", conn)
st.dataframe(df)

# Orders Data
st.subheader("Orders Data")
df2 = pd.read_sql_query("SELECT * FROM orders", conn)
st.dataframe(df2)

# 🔥 AI Query Section (NEW ADD)
st.subheader("Ask Questions")

query = st.text_input("Ask something about data:")

if query:
    if "customers" in query.lower():
        st.write(df)
    elif "orders" in query.lower():
        st.write(df2)
    else:
        st.write("Sorry, I don't understand")