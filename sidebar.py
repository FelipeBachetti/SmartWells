import streamlit as st

def activate_sidebar(current_page):
    with st.sidebar:
        st.image('data\\LOGO02.png', use_column_width=True)
        home = st.button('Home', use_container_width=True)
        page2 = st.button('Page 2', use_container_width=True)
        
        if(home and current_page != 1):
            return 1
        elif(page2 and current_page != 2):
            return 2
        else:
            return current_page