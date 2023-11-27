import streamlit as st
import db_connection
from email_validator import validate_email, EmailNotValidError
import page_manager as page
import datetime
import re

#Verifica se é um email válido usando a biblioteca email_validator
def check_email(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return True
    except EmailNotValidError as e:
        return False
    
def login(column):
    #Cria a aba para login
    with column:
        with st.expander('Login:',True):
            st.header("Login into your account:")

            #Campos para email e senha
            email = st.text_input("Email:", key="text14")
            password = st.text_input("Password:", type="password", key="text15")

            #Colunas para posicionar o botão no meio
            c1,c2,c3,c4,c5 = st.columns(5)
            with c3:
                #Botão para continuar
                clicked = st.button("Continue", key="button2", use_container_width=True)

            #Ao clicar no botão
            if(clicked):
                with st.spinner("Please wait..."):
                    #Verifica se os campos possuem informações
                    if(email != "" and password != ""):
                        #Busca o usuário no banco e, caso a senha esteja correta, adiciona suas informações a uma variável de sessão
                        if db_connection.db_find_user(email, password):
                            if "user" not in st.session_state:
                                st.session_state.user = db_connection.db_find_user(email, password)
                            #Atualiza um timestamp com o horário de login e prossegue
                            if st.session_state.user:
                                db_connection.update_login_timestamp(email)
                                register_company(False)
                                return True
                        else:
                            st.error("Incorrect credentials.", icon="🚨")
                    else:
                        st.error("Please fill in all required fields.", icon="🚨")

def sign_up(column):
    #Cria aba para registro de usuário
    with column:
        with st.expander('Sign Up:', True):
            st.header("Sign up a new user:")
            #Pede todas informações de login
            pid = st.text_input("Personal ID (CPF, SSN, etc.):", key="text0", max_chars=20)
            email = st.text_input("Email:", key="text1", max_chars=100)
            password = st.text_input("Password:", type="password", key="text2", max_chars=100)
            confirm_password = st.text_input("Confirm password:", type="password", key="text31", max_chars=100)
            name = st.text_input("Full name:", key="text3", max_chars=200)

            #Procura por empresas no banco e adiciona em um combo box
            companyList = db_connection.get_list('company', 'marketname', False)
            company = ""
            if(companyList):
                company = st.selectbox('Company: ', companyList, key="text29")
            #Botão para adicionar nova empresa
            add_company = st.button("Add company", key="button3", use_container_width=True)

            #Separa as caixas de texto em duas colunas
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Professional phone number:", key="text4", max_chars=20)
                birthDate = st.date_input("Date of Birth:", key="text5", format='DD/MM/YYYY', min_value=datetime.date(1920, 1, 1), max_value=datetime.date.today())
                countryList = db_connection.get_list('country', 'name', False)
                country = st.selectbox('Country: ', countryList, key="text6", index=22)
                state = st.text_input("State/Province:", key="text7", max_chars=50)
                complement = st.text_input("Complement (optional):", key="text8", max_chars=20) #opt
            with col2:
                phoneWpp = st.text_input("Whatsapp phone number (optional):", key="text9", max_chars=20) #opt
                timeList = db_connection.get_list('timeZoneEnum', 'timeZoneEnum', True)
                timeZone = st.selectbox('Time zone: ', timeList, key="text10", index=23)
                zipCode = st.text_input("Zip Code:", key="text11", max_chars=20)
                city = st.text_input("City:", key="text12", max_chars=20)
                number = st.number_input("Number:", key="number0", min_value=0, max_value=100000)
            
            street = st.text_input("Street:", key="text13", max_chars=100)

            #Colunas para posicionar o botão no meio
            c1,c2,c3,c4,c5 = st.columns(5)
            with c3:
                clicked = st.button("Continue", key="button1", use_container_width=True)

            #Ao clicar no botão de continuar
            if(clicked):
                with st.spinner("Please wait..."):
                    #Verifica se o email é válido
                    if(check_email(email)):
                        #Verifica se as caixas obrigatórias foram preenchidas
                        if(company != "" and email != "" and password != "" and name != "" and phone != "" and pid != "" and state != "" and zipCode != "" and city != "" and number != "" and street != ""):
                            #Limpa certas strings e deixa apenas números
                            pattern = r'[^0-9]'
                            pid = re.sub(pattern, '', pid)
                            phone = re.sub(pattern, '', phone)
                            phoneWpp = re.sub(pattern,'', phoneWpp)
                            #Verifica se esse id já está sendo usado
                            if(not db_connection.db_id_exists(pid)):
                                #Verifica se esse email já está sendo usado
                                if(not db_connection.db_email_exists(email)):
                                    if(password == confirm_password):
                                        #Verifica se a senha é válida
                                        if(check_valid_password(password)):
                                            #Pega o id da empresa com base no nome escolhido no combo box
                                            cid = db_connection.db_get_company_id(company)
                                            #Insere o usuário
                                            if(db_connection.db_insert_user(pid, cid, name, phone, phoneWpp, email, password, country, state, city, zipCode, complement, number, timeZone, birthDate, street)):  
                                                if "user" not in st.session_state:
                                                    st.session_state.user = db_connection.db_find_user(email, password)
                                                return True
                                            else:
                                                st.error("We're experiencing database connection issues. Please try again later.", icon="🚨")
                                        else:
                                            st.error("Password must have at least 8 characters, one uppercase letter, one lowercase letter, one digit and one special character.", icon="🚨")
                                    else:
                                        st.error("Passwords don't match", icon="🚨")
                                else:
                                    st.error("An account with this email already exists.", icon="🚨")
                            else:
                                st.error("An account with this personal id already exists.", icon="🚨")
                        else:
                            st.error("Please fill in all required fields.", icon="🚨")
                    else:
                        st.error("Invalid email address.", icon="🚨")

            #Essa parte cuida da sidebar de inserção de empresa, é necessário para fechá-la quando acabar o processo
            if "company_sidebar" not in st.session_state:
                st.session_state.company_sidebar = False

            if(add_company and st.session_state.company_sidebar == False):
                st.session_state.company_sidebar = True
            elif(add_company and st.session_state.company_sidebar == True):
                st.session_state.company_sidebar = False

            if(st.session_state.company_sidebar == True):
                register_company(True)
        
#Checa se a senha é válida baseado na expressão regular. Parametros:
#Pelo menos uma maiuscula
#Pelo menos uma minuscula
#Pelo menos um número
#Pelo menos um caracter especial
#Pelo menos oito caracteres no total
def check_valid_password(password):
    password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    if re.match(password_regex, password):
        return True
    return False

#O registro de empresa segue a mesma lógica do registro de usuario
def register_company(open):
    clicked = False
    if(open):
        with st.sidebar:
            st.header("Company information:")
            oficialname = st.text_input("Oficial name:", key="text16", max_chars=200)
            marketname = st.text_input("Market name:", key="text17", max_chars=200)
            
            regid = st.text_input("Company registration number (EIN, CNPJ, etc.):", key="text18", max_chars=20)
            status = st.text_input("Company status (optional):", key="text20", max_chars=200)
            phone = st.text_input("Phone number:", key="text19", max_chars=20)
            city = st.text_input("City:", key="text22", max_chars=50)
            countryList = db_connection.get_list('country', 'name', False)
            country = st.selectbox('Country: ', countryList, key="text30", index=22)
            zipcode = st.text_input("Zip code:", key="text23", max_chars=20)
            state = st.text_input("State:", key="text21", max_chars=50)
            number = st.number_input("Number:", key="number1", min_value=0, max_value=100000)
            complement = st.text_input("Complement:", key="text25", max_chars=20)

            street = st.text_input("Street:", key="text24", max_chars=100)

            st.header("Contact person information:")
            cpfullname = st.text_input("Full name:", key="text26", max_chars=200)
            cpphone = st.text_input("Phone number:", key="text27", max_chars=20)
            cpemail = st.text_input("Email:", key="text28", max_chars=20)

            clicked = st.button("Continue", key="button4", use_container_width=True)


    if(clicked):
            with st.spinner("Please wait..."):
                if(country != "" and oficialname != "" and marketname != "" and regid != "" and phone != "" and zipcode != "" and state != "" and cpfullname != "" and city != "" and cpphone != "" and street != "" and cpemail != "" and number != ""):
                    pattern = r'[^0-9]'
                    regid = re.sub(pattern, '', regid)
                    if(not db_connection.db_regid_exists(regid)):
                        if(db_connection.db_insert_company(regid, oficialname, marketname, phone, status, cpfullname, cpphone, cpemail, state, city, zipcode, complement, street)):  
                            st.session_state.company_sidebar = False
                            register_company(False)
                            st.experimental_rerun()
                        else:
                            st.error("We're experiencing database connection issues. Please try again later.", icon="🚨")
                    else:
                        st.error("A company with this registration number already exists.", icon="🚨")
                else:
                    st.error("Please fill in all required fields.", icon="🚨")

def register_well():
    st.title("Well Registration Page")
    st.header("User information:")
    if "company_sidebar" in st.session_state:
        userid = st.session_state.user.id
        st.text_input("Personal registration number:", value=userid, key="text32", max_chars=20, disabled=True)
        cid = st.session_state.user.cid
        st.text_input("Company registration number:", value=cid, key="text33", max_chars=20, disabled =True)
    
    st.header("Well information:")
    name = st.text_input("Well name:", key="text34", max_chars=200)
    description = st.text_area("Description (optional):", key="text35", max_chars=200) #opt
    operatingCompany = st.text_input("Operating Company:", key="text38", max_chars=200)
    soundingCompany = st.text_input("Sounding Company:", key="text39", max_chars=200)
    drillingCompany = st.text_input("Drilling Company:", key="text40", max_chars=200)

    c1, c2 = st.columns(2)

    with c1:
        status = st.text_input("Status (optional):", key="text36", max_chars=200) #opt
        envList = db_connection.get_list('', 'enviromentenum', True)
        environment = st.selectbox('Environment: ', envList, key="text41")
        typeList = db_connection.get_list('', 'welltypeenum', True)
        wellType = st.selectbox('Well type: ', typeList, key="text42")
        depth = float(st.number_input("Depth:", key="text44", min_value=0.0, max_value=999999.99, value=0.0))
        block = st.text_input("Block (optional):", key="text47", max_chars=20)#opt
    with c2: 
        inclinationList = db_connection.get_list('', 'inclinationenum', True)
        inclination = st.selectbox('Inclination: ', inclinationList, key="text43")
        resList = db_connection.get_list('', 'reservoirtypeenum', True)
        reservoir = st.selectbox('Reservoir type: ', resList, key="text49")
        waterDepth = float(st.number_input("Water depth:", key="text45", min_value=0.0, max_value=999999.99, value=0.0))
        wellCode = int(st.number_input("Code:", key="text46", min_value=0, max_value=999999, value=0))
        field = st.text_input("Field (optional):", key="text48", max_chars=20)#opt

    c1,c2,c3,c4,c5 = st.columns(5)
    with c3:
        clicked = st.button("Continue", key="button5", use_container_width=True)

    if(clicked):
            with st.spinner("Please wait..."):
                if(name != "", operatingCompany != "", soundingCompany != "", drillingCompany != "", environment != "", wellType != "", depth != "", waterDepth != "", reservoir != "", inclination != "", wellCode != ""):
                    if(db_connection.db_insert_well(userid, cid, name, description, status, operatingCompany, soundingCompany, drillingCompany, environment, wellType, depth, waterDepth, wellCode, block, reservoir, field, inclination)):
                        st.success("Well added!")
                    else:
                            st.error("We're experiencing database connection issues. Please try again later.", icon="🚨")
                else:
                    st.error("Please fill in all required fields.", icon="🚨")