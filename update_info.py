import streamlit as st
import db_connection
import datetime
import registration as res
import re
import extra_streamlit_components as stx

def update_user_info():
        email = st.session_state.user.email
        info = db_connection.db_find_user(email)
        col1, col2 = st.columns(2)
        with col1:
            st.header("Update user information:")
            pid = st.text_input("Personal ID (CPF, SSN, etc.):", key="text80", max_chars=20, disabled=True, value=info[0])
            email = st.text_input("Email:", key="text81", max_chars=100, value=info[5])
            name = st.text_input("Full name:", key="text83", max_chars=200, value=info[2])

            #Procura por empresas no banco e adiciona em um combo box
            companyList = db_connection.get_list('company', 'marketname', False)
            company = ""
            if(companyList):
                marketname = db_connection.query_command(f"SELECT marketname FROM company WHERE registrationnumber='{(info[1])}';")
                company = st.selectbox('Company: ', companyList, key="text829", index=counter(companyList, marketname[0]), disabled=True)

            #Separa as caixas de texto em duas colunas
            c1, c2 = st.columns(2)
            with c1:
                phone = st.text_input("Professional phone number:", key="text84", max_chars=20, value=info[3])
                birthDate = st.date_input("Date of Birth:", key="text85", format='DD/MM/YYYY', min_value=datetime.date(1920, 1, 1), max_value=datetime.date.today(), value=info[14])
                countryList = db_connection.get_list('country', 'name', False)
                country = st.selectbox('Country: ', countryList, key="text86", index=counter(countryList, info[7]))
                state = st.text_input("State/Province:", key="text87", max_chars=50, value=info[8])
                complement = st.text_input("Complement (optional):", key="text88", max_chars=20, value=info[11]) #opt
            with c2:
                phoneWpp = st.text_input("Whatsapp phone number (optional):", key="text89", max_chars=20, value=info[4]) #opt
                timeList = db_connection.get_list('timeZoneEnum', 'timeZoneEnum', True)
                timeZone = st.selectbox('Time zone: ', timeList, key="text810", index=counter(timeList, info[13]))
                zipCode = st.text_input("Zip Code:", key="text811", max_chars=20, value=info[10])
                city = st.text_input("City:", key="text812", max_chars=20, value=info[9])
                number = st.number_input("Number:", key="number80", min_value=0, max_value=100000, value=info[12])
            
            street = st.text_input("Street:", key="text813", max_chars=100, value=info[16])

            st.subheader("Enter your password to confirm the update:")
            password = st.text_input("Password:", type="password", key="text82", max_chars=100)
            clicked = st.button("Continue", key="button82", use_container_width=True)

            if(clicked):
                with st.spinner("Please wait..."):
                    if db_connection.db_find_user(info[5], password):
                        if(res.check_email(email)):
                            if(company != "" and email != "" and name != "" and phone != "" and pid != "" and state != "" and zipCode != "" and city != "" and number != "" and street != "" and password != ""):
                                pattern = r'[^0-9]'
                                pid = re.sub(pattern, '', pid)
                                phone = re.sub(pattern, '', phone)
                                phoneWpp = re.sub(pattern,'', phoneWpp)
                                #Verifica se esse email já está sendo usado
                                if(email == info[5] or not db_connection.db_email_exists(email)):
                                    #Insere o usuário
                                    if(db_connection.db_update_user(pid, name, phone, phoneWpp, email, country, state, city, zipCode, complement, number, timeZone, birthDate, street)):  
                                        st.session_state.user = db_connection.db_find_user(email, password)
                                        return True
                                    else:
                                        st.error("We're experiencing database connection issues. Please try again later.", icon="🚨")
                                else:
                                    st.error("An account with this email already exists.", icon="🚨")
                            else:
                                st.error("Please fill in all required fields.", icon="🚨")
                        else:
                            st.error("Invalid email address.", icon="🚨")
                    else:
                        st.error("Invalid password.", icon="🚨")

        with col2:
            st.header("Update user password:")
            st.subheader("Enter your new password:")
            new_password0 = st.text_input("Password:", type="password", key="text822", max_chars=100)
            new_password1 = st.text_input("Confirm password:", type="password", key="text823", max_chars=100)

            st.subheader("Enter your current password to confirm the update:")
            password = st.text_input("Password:", type="password", key="text824", max_chars=100)

            clicked = st.button("Continue", key="button83", use_container_width=True)

            if(clicked):
                with st.spinner("Please wait..."):
                    if(new_password0!="" and new_password1!="" and password!=""):
                        if db_connection.db_find_user(info[5], password):
                            if(new_password0 == new_password1):
                                if(res.check_valid_password(new_password0)):
                                    if(db_connection.db_update_password(info[5], new_password0)):
                                        st.success('Password updated!', icon="✅")
                                else:
                                     st.error("Password must have at least 8 characters, one uppercase letter, one lowercase letter, one digit and one special character.", icon="🚨")
                            else:
                                st.error("Passwords don't match.", icon="🚨")
                        else:
                            st.error("Invalid password.", icon="🚨")
                    else:
                        st.error("Please fill in all required fields.", icon="🚨")


def counter(list, item):
    i = 0
    for n in list:
        if(n == item):
            return i
        else:
            i+=1