import psycopg2 as psy
import bcrypt
import streamlit as st
import datetime
from User import User_class

#Cria as tables no banco
def db_init():
	conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
	cur = conn.cursor()

	if(conn.status==1):
		cur.execute("""
			CREATE TABLE IF NOT EXISTS Continent (
				name VARCHAR(20) PRIMARY KEY
			);
			  
			CREATE TABLE IF NOT EXISTS Country (
				name VARCHAR(50) PRIMARY KEY,
			  	continent VARCHAR(20),
			  	idFormat VARCHAR(20),
			  	CompanyRegistrationFormat VARCHAR(20),
			  	FOREIGN KEY (continent) REFERENCES Continent(name)
			);
			  
			CREATE TYPE timeZoneEnum AS ENUM ('International Date Line West','Coordinated Universal Time-11', 'Hawaii Time', 'Alaska Time','Baja California	time','Pacific Time time','Chihuahua, La Paz, Mazatlan time','Arizona time','Mountain Time (US and Canada)','Central America time','Central Time','Saskatchewan time','Guadalajara, Mexico City, Monterey time','Bogota, Lima, Quito time','Indiana time (East)','Eastern Time (US and Canada)','Caracas time','Atlantic Time (Canada)','Asuncion time','Georgetown, La Paz, Manaus, San Juan time','Cuiaba time','Santiago time','Newfoundland time','Brasilia time','Greenland time','Cayenne, Fortaleza time','Buenos Aires time','Montevideo time','Coordinated Universal Time-2','Cape Verde time','Azores time','Casablanca time','Monrovia, Reykjavik time','Dublin, Edinburgh, Lisbon, London time','Coordinated Universal Time','Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna time','Brussels, Copenhagen, Madrid, Paris time','West Central Africa time','Belgrade, Bratislava, Budapest, Ljubljana, Prague time','Sarajevo, Skopje, Warsaw, Zagreb time','Windhoek time','Athens, Bucharest, Istanbul time','Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius time','Cairo time','Damascus time','Amman time','Harare, Pretoria time','Jerusalem time','Beirut time','Baghdad time','Minsk time','Kuwait, Riyadh time','Nairobi	 time','Tehran time','Moscow, St. Petersburg, Volgograd time','Tbilisi time','Yerevan time','Abu Dhabi, Muscat time','Baku time','Port Louis time','Kabul time','Tashkent time','Islamabad, Karachi time','Sri Jayewardenepura Kotte time','Chennai, Kolkata, Mumbai, New Delhi time','Kathmandu time','Astana time','Dhaka time','Yekaterinburg time','Yangon time','Bangkok, Hanoi, Jakarta time','Novosibirsk time','Krasnoyarsk time','Ulaanbaatar time','Beijing, Chongqing, Hong Kong, Urumqi time','Perth time','Kuala Lumpur, Singapore time','Taipei time','Irkutsk time','Seoul time','Osaka, Sapporo, Tokyo time','Darwin time','Adelaide time','Hobart time','Yakutsk time','Brisbane time','Guam, Port Moresby time','Canberra, Melbourne, Sydney time','Vladivostok time','Solomon Islands, New Caledonia time','Coordinated Universal Time+12','Fiji, Marshall Islands time','Magadan time','Auckland, Wellington time','Nukualofa time','Samoa time');
			  
			CREATE TYPE enviromentEnum AS ENUM ('OnShore','OffShore');
			  
			CREATE TYPE wellTypeEnum AS ENUM ('Exploratory','Producer', 'Other');
			  
			CREATE TYPE reservoirTypeEnum AS ENUM ('Dry','Oil','Gas','Hydrogen', 'Water', 'Geothermal', 'Other');
			  
			CREATE TYPE inclinationEnum AS ENUM ('Directional','Vertical');
			  
			CREATE TABLE IF NOT EXISTS User_ (
				personalId VARCHAR(20) PRIMARY KEY NOT NULL,
				CompanyId VARCHAR(20),
				fullName VARCHAR(200),
				phoneProfessional VARCHAR(20),
			  	phoneWhatsapp VARCHAR(20),
				email VARCHAR(100),
				password BYTEA,
			  	country VARCHAR(50),
				state VARCHAR(50),
			  	city VARCHAR(50),
			  	zipcode VARCHAR(20),
			  	complement VARCHAR(20),
			  	number VARCHAR(10),
			  	timeZone timeZoneEnum,
			  	dateOfBirth DATE,
	      		last_login TIMESTAMP,
			  	FOREIGN KEY (country) REFERENCES Country(name)
			);

			CREATE TABLE IF NOT EXISTS Company (
				registrationNumber VARCHAR(20) PRIMARY KEY NOT NULL,
				wellId VARCHAR(20),
				oficialName VARCHAR(200),
			  	marketName VARCHAR(200),
				phone VARCHAR(20),
			  	status VARCHAR(200),
			  	contactPersonFullName VARCHAR(200),
			  	contactPersonPhone VARCHAR(20),
			  	contactPersonEmail VARCHAR(100),
				state VARCHAR(50),
			  	city VARCHAR(50),
			  	zipCode VARCHAR(20),
			  	complement VARCHAR(20),
			  	street VARCHAR(100)
			);

			CREATE TABLE IF NOT EXISTS Well (
				id SERIAL PRIMARY KEY NOT NULL,
				userId VARCHAR(20),
				companyId VARCHAR(20),
				name VARCHAR(200),
				description VARCHAR(300),
				status VARCHAR(200),
			  	opertatingCompany VARCHAR(200),
			  	soundingCompany VARCHAR(200),
			  	drillingCompany VARCHAR(200),
			  	enviroment enviromentEnum,
			  	wellType wellTypeEnum,
			  	depth DOUBLE PRECISION,
			  	waterDepth DOUBLE PRECISION,
			  	wellCode BIGINT,
			  	block VARCHAR(20),
			  	reservoirType reservoirTypeEnum,
			  	field VARCHAR(20),
			  	inclination inclinationEnum,
				FOREIGN KEY (userId) REFERENCES User_(personalId),
				FOREIGN KEY (companyId) REFERENCES Company(registrationNumber)
			);

			CREATE TABLE IF NOT EXISTS Data_ (
				id SERIAL PRIMARY KEY NOT NULL,
				wellId BIGINT,
				rop DOUBLE PRECISION,
				mse DOUBLE PRECISION,
				dwob DOUBLE PRECISION,
				swob DOUBLE PRECISION,
				srpm DOUBLE PRECISION,
			  	crpm DOUBLE PRECISION,
				flow DOUBLE PRECISION,
			  	stor DOUBLE PRECISION,
			  	dtor DOUBLE PRECISION,
			  	tvd DOUBLE PRECISION,
			  	md DOUBLE PRECISION,
				FOREIGN KEY (wellId) REFERENCES Well(id)
			);
			  
			CREATE TABLE IF NOT EXISTS Company_User (
				companyId VARCHAR(20),
				userId VARCHAR(20),
				PRIMARY KEY (companyId, userId),
				FOREIGN KEY (companyId) REFERENCES Company(registrationNumber),
				FOREIGN KEY (userId) REFERENCES User_(personalId)
			);
			  
			  CREATE TABLE IF NOT EXISTS WellUser (
				wellId BIGINT,
				userId VARCHAR(20),
				PRIMARY KEY (wellId, userId),
				FOREIGN KEY (wellId) REFERENCES Well(id),
				FOREIGN KEY (userId) REFERENCES User_(personalId)
			);
			  
			CREATE TABLE IF NOT EXISTS Company_Well (
				companyId VARCHAR(20),	
			  	wellId BIGINT,
				PRIMARY KEY (companyId, wellId),
			  	FOREIGN KEY (companyId) REFERENCES Company(registrationNumber),
				FOREIGN KEY (wellId) REFERENCES Well(id)
			);
			  
			CREATE TABLE IF NOT EXISTS Data_Well (
				dataId BIGINT,	
			  	wellId BIGINT,
				PRIMARY KEY (dataId, wellId),
			  	FOREIGN KEY (dataId) REFERENCES Data_(id),
				FOREIGN KEY (wellId) REFERENCES Well(id)
			);

			BEGIN;

				ALTER TABLE User_ 
					ADD CONSTRAINT fk_user_company FOREIGN KEY (CompanyId) REFERENCES Company(registrationNumber) DEFERRABLE INITIALLY DEFERRED;

			COMMIT;
		""")
		conn.commit()
		cur.close()
		conn.close()
		return True
	else:
		cur.close()
		conn.close()
		return False
	
#adiciona os continentes na table Continent
def add_continents():
	conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
	cur = conn.cursor()

	if(conn.status==1):
		cur.execute("""
			  INSERT INTO Continent (name) VALUES ('South America');
			  INSERT INTO Continent (name) VALUES ('North America');
			  INSERT INTO Continent (name) VALUES ('Europe');
			  INSERT INTO Continent (name) VALUES ('Africa');
			  INSERT INTO Continent (name) VALUES ('Asia');
			  INSERT INTO Continent (name) VALUES ('Oceania');
		""")
		conn.commit()
		cur.close()
		conn.close()
		return True
	else:
		cur.close()
		conn.close()
		return False
	
#adiciona países na table Country
#A lista de países se encontra em countries.txt
#Nome pais/Continente/Formato cpf/formato cnpj
def add_countries():
		conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
		cur = conn.cursor()

		if(conn.status==1):
			with open("data\\countries.txt", 'r') as file:
				file_contents = file.read()
				
				country_list = file_contents.split('\n')
				
				for country in country_list:
					info_list = country.split('/')
					query = """INSERT INTO Country (name, continent, idFormat, companyRegistrationFormat) VALUES (%s,%s,%s,%s);"""
					data = (info_list[0], info_list[1], info_list[2], info_list[3])
					cur.execute(query, data)

			conn.commit()
			cur.close()
			conn.close()
			return True
		else:
			cur.close()
			conn.close()
			return False

#insere um usuário ao banco
def db_insert_user(pid, cid, fullname, phonePro, phoneWpp, email, password, country, state, city, zipcode, complement, number, timezone, dateofbirth):
	conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
	cur = conn.cursor()

	if(conn.status==1):
		query = """INSERT INTO user_ (personalid, companyid, fullname, phoneprofessional, phonewhatsapp, email, password, country, state, city, zipcode, complement, number, timezone, dateofbirth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

		password_bytes = password.encode('utf-8')
		salt = bcrypt.gensalt(rounds=12)
		hashed = bcrypt.hashpw(password_bytes, salt)

		data = (pid, cid, fullname, phonePro, phoneWpp, email, hashed, country, state, city, zipcode, complement, number, timezone, dateofbirth)
		cur.execute(query, data)

		conn.commit()

		cur.close()
		conn.close()
		return True
	else:
		cur.close()
		conn.close()
		return False
	
#Procura um usuário no banco e verifica sua senha
def db_find_user(email, password):
	conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
	cur = conn.cursor()

	if(conn.status==1):
		query = "SELECT * FROM user_ WHERE email = %s;"
		cur.execute(query, (email,))
		user = cur.fetchone()
		if(user):
			hashed = user[6].tobytes()
			if bcrypt.checkpw(password.encode('utf-8'), hashed):
				cur.close()
				conn.close()
				u = User_class(id = user[0], name = user[2], phone = user[4], email = user[5])
				return u
	cur.close()
	conn.close()

#checa se o email já existe
def db_email_exists(email):
	conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
	cur = conn.cursor()

	if(conn.status==1):
		query = "SELECT * FROM user_ WHERE email = %s;"
		cur.execute(query, (email,))
		user = cur.fetchone()
		cur.close()
		conn.close()
		if(user):
			return True
		else:
			return False
		
def db_id_exists(pid):
	conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
	cur = conn.cursor()

	if(conn.status==1):
		query = "SELECT * FROM user_ WHERE personalid = %s;"
		cur.execute(query, (pid,))
		user = cur.fetchone()
		cur.close()
		conn.close()
		if(user):
			return True
		else:
			return False

#atualiza o timestamp de login
def update_login_timestamp(email):
	conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
	cur = conn.cursor()

	if(conn.status==1):
		query = f"UPDATE user_ SET last_login = %s WHERE email = %s"
		current_time = datetime.datetime.now()
		cur.execute(query, (current_time, email))
	conn.commit()
	cur.close()
	conn.close()

#devolve uma coluna no formato de lista
def get_list(table, column, enum):
	conn = psy.connect(database = "smartwellsdatabase", host = "localhost", user = "postgres", password = "7246", port = "5432")
	cur = conn.cursor()

	if(conn.status==1):
		if(enum):
			query = f"SELECT unnest(enum_range(NULL::{column}))::text;"
		else:
			query = f"SELECT {column} FROM {table} ORDER BY {column} ASC;"
		cur.execute(query)
		rows= cur.fetchall()
		cur.close()
		conn.close()
		if(rows):
			info = [row[0] for row in rows]
			return info
	return None
	
