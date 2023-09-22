import streamlit as st

st.set_page_config(page_title="Smart Wells", page_icon=":oil_drum:", layout="centered", initial_sidebar_state="auto", menu_items=None)
css='''
<style>
    section.main > div {max-width:60rem}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

import pandas as pd
import json
from pathlib import Path
import page_manager as page
import db_connection

# db_connection.db_clean_tables()
# db_connection.db_init()

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

page.page_transitions()

#db_connection.add_continents()
#db_connection.add_countries() 