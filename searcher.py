import streamlit as st
import pandas as pd
import db_connection as db

def search_wells():
    df = pd.DataFrame(db.get_list(table = "well"))
    st.write(df)

