import streamlit as st
import db_connection
from email_validator import validate_email, EmailNotValidError
import page_manager as page
import datetime

def check_email(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError as e:
        return False
    
def login():
    with st.expander("Login", True):
        st.header("Login into your account:")
        email = st.text_input("Email:", key="text6")
        password = st.text_input("Password:", type="password", key="text7")

        clicked = st.button("Continue", key="button2")

        if(clicked):
            with st.spinner("Please wait..."):
                if(email != "" and password != ""):
                    if "user" not in st.session_state:
                        st.session_state.user = db_connection.db_find_user(email, password)
                    if st.session_state.user:
                        db_connection.update_login_timestamp(email)
                        return True
                    else:
                        st.error("Incorrect credentials.", icon="🚨")
                else:
                    st.error("Please fill in all required fields.", icon="🚨")

def sign_up():
    with st.expander("Sign Up", False):
        st.header("Sign up a new user:")
        pid = st.text_input("Personal ID:", key="text0")
        email = st.text_input("Email:", key="text1")
        password = st.text_input("Password:", type="password", key="text2")
        name = st.text_input("Full name:", key="text3")
        col1, col2 = st.columns(2)
        countryList = db_connection.get_list('country', 'name', False)
        with col1:
            phone = st.text_input("Professional phone number:", key="text4")
            birthDate = st.date_input("Date of Birth:", format='DD/MM/YYYY', min_value=datetime.date(1920, 1, 1), max_value=datetime.date.today())
            country = st.selectbox('Country: ', countryList, index=22)
            state = st.text_input("State/Province:")
            complement = st.text_input("Complement (optional):") #opt
        timeList = db_connection.get_list('timeZoneEnum', 'timeZoneEnum', True)
        with col2:
            phoneWpp = st.text_input("Whatsapp phone number (optional):") #opt
            timeZone = st.selectbox('Time zone: ', timeList, index=23)
            zipCode = st.text_input("Zip Code:")
            city = st.text_input("City:")
            number = st.text_input("Number:")
        
        street = st.text_input("Street:")

        clicked = st.button("Continue", key="button1")

        if(clicked):
            with st.spinner("Please wait..."):
                if(check_email(email)):
                    if(email != "" and password != "" and name != "" and phone != "" and pid != "" and state != "" and zipCode != "" and city != "" and number != "" and street != ""):
                        if(not db_connection.db_id_exists(pid)):
                            if(not db_connection.db_email_exists(email)):
                                if(db_connection.db_insert_user(pid, '0', name, phone, phoneWpp, email, password, country, state, city, zipCode, complement, number, timeZone, birthDate)):  
                                    if "user" not in st.session_state:
                                        st.session_state.user = db_connection.db_find_user(email, password)
                                else:
                                    st.error("We're experiencing database connection issues. Please try again later.", icon="🚨")
                            else:
                                st.error("An account with this email already exists.", icon="🚨")
                        else:
                            st.error("An account with this personal id already exists.", icon="🚨")
                    else:
                        st.error("Please fill in all required fields.", icon="🚨")
                else:
                    st.error("Invalid email address.", icon="🚨")
