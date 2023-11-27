import streamlit as st
import registration as registration
import file_uploader as file
import update_info
import extra_streamlit_components as stx

def next_page(placeholder):
   placeholder.empty()
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
    with placeholder:
        if(st.session_state.page == 0):
            with st.container():
                c1, c2 = st.columns(2)
                if("user" in st.session_state or registration.sign_up(c2) or registration.login(c1)):
                    next_page(placeholder)      
                    st.rerun() 
        elif(st.session_state.page == 1):
            with st.container():
                    chosen_id = stx.tab_bar(data=[
                        stx.TabBarItemData(id=1, title="Home", description="Upload your data"),
                        stx.TabBarItemData(id=2, title="Well", description="Well registration"),
                        stx.TabBarItemData(id=3, title="Account", description="Manage password and user info"),
                    ], default=1)
                    if f"{chosen_id}"=='1':
                        if "user" in st.session_state:
                            st.write("Welcome, " + (st.session_state.user.name).rsplit(' ')[0])
                        file.init_df()
                    if f"{chosen_id}"=='2':
                        registration.register_well()
                    if f"{chosen_id}"=='3':
                        update_info.update_user_info()
