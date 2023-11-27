import streamlit as st

st.set_page_config(page_title="Smart Wells", page_icon=":oil_drum:", layout="wide", initial_sidebar_state="auto", menu_items=None)
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.markdown("""
<style>
            
    /*.stApp {
		background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
		background-size: cover;
	}*/

	.stTabs [data-baseweb="tab-list"] {
		gap: 4px;
    }

	.stTabs [data-baseweb="tab"] {
		height: 75px;
        white-space: pre-wrap;
		background-color: #F0F2F6;
		border-radius: 40px 40px 0px 0px;
		gap: 1px;
		padding-top: 10px;
		padding-bottom: 10px;
        width: 160px;
    }

	.stTabs [aria-selected="true"] {
  		background-color: #ff4d4d;
        color:#FFFFFF;
	}
            
	button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
		font-size: 25px;
        font-family:Garamond
	}

</style>""", unsafe_allow_html=True)

import pandas as pd
import json
from pathlib import Path
import page_manager as page
import db_connection

# db_connection.db_clean_tables()
# db_connection.db_init()

page.page_transitions()

# db_connection.add_continents()
# db_connection.add_countries() 