import streamlit as st
import registration as registration
import file_uploader as file
import sidebar as sb

def next_page(placeholder):
   placeholder.empty()
   sb.activate_sidebar(st.session_state.page)
   if(st.session_state.page < 4):
       st.session_state.page += 1
    
    

def previous_page(placeholder):
   placeholder.empty()
   if(st.session_state.page > 0):
      st.session_state.page -= 1

def change_page(placeholder, page):
    placeholder.empty()
    st.session_state.page = page

placeholder = st.empty()

def page_transitions():
    if "page" not in st.session_state:
        st.session_state.page = 0
    if(st.session_state.page != 0):
        new_page = sb.activate_sidebar(st.session_state.page)
        if(new_page != st.session_state.page):
            change_page(placeholder, new_page)
    with placeholder:
        if(st.session_state.page == 0):
            with st.container():
                if("user" in st.session_state or registration.sign_up() or registration.login()):
                    next_page(placeholder)       
        if(st.session_state.page == 1):
            with st.container():
                if "user" in st.session_state:
                    st.write("Welcome, " + (st.session_state.user.name).rsplit(' ', 1)[0])
                file.init_df()
        if(st.session_state.page == 2):
            with st.container():
                st.write("page 2")