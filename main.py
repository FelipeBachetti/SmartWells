import streamlit as st


import psycopg2


@st.experimental_singleton
def init_connection():
    return st.experimental_get_query_params().type(**secrets)

conn = init_connection()
# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
rows = run_query("SELECT * from user_;")
# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
