import streamlit as st
from json import loads
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from io import BytesIO
from streamlit_extras.chart_container import chart_container
from streamlit_extras.dataframe_explorer import dataframe_explorer
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
from datetime import datetime
import altair as alt

def init_df():  
    #Nome das colunas que serão aceitas (a fazer)
    column_names = [
    "DEPT", "DVER", "BDIA", "ROPA", "HKLA", "HKLX", "WOBA", "TQA", "TQX", "TQM",
    "RPMB", "SPPA", "TVA", "MFOA", "MFIA", "MDOA", "MDIA", "MTOA", "MTIA", "ECDT",
    "BDTI", "BDDI", "BRVC", "TCTI", "FPPG", "DXC", "GASX", "HSX", "MTHA", "ETHA",
    "PRPA", "IBTA", "NBTA", "IPNA", "NPNA", "C1C2", "C1C3", "C1C4", "C1C5", "LITH",
    "CCAL", "CDOL", "WLFL", "WLCT"
    ]

    df = pd.DataFrame(columns=column_names)
    uploaded_df = uploader(df)
    if not uploaded_df is None and not uploaded_df.empty:
        df = uploaded_df
    df = dataframe_explorer(df, case=False)
    df = st.data_editor(df, num_rows='dynamic')

    if not df.empty:
        plot_parameters()
    plot_chart(df)

def uploader(df):
    #Aceita arquivos enviados pelo usuário (apenas csv por enquanto)
    file = st.file_uploader("Upload de arquivo: ", ['csv', 'json'])

    if file:
        match file.type.split('/'):
            case 'application', 'json':
                st.json(loads(file.read()))
            case 'text', 'csv':
                df = pd.read_csv(file)
                columns = df.columns
                for c in columns:
                    c.replace(" ", "")
                    c.upper()
                df.columns = columns
        return df

            
def plot_parameters():
    #Pede ao usuário os parametros do gráfico a ser plotado
    with st.expander("Plot: ", False):
        x_ = st.session_state.x_ if 'x_' in st.session_state else ''
        y_ = st.session_state.y_ if 'y_' in st.session_state else ''
        col1, col2 = st.columns(2)
        with col1:
            x_ = st.text_input("Enter the x value: ", key="text1")
        with col2:
            y_ = st.text_input("Enter the y value: ", key="text2")
        col1, col2 = st.columns(2)
        with col1:
            global line
            line = st.button("Plot line chart", key="button2", use_container_width=True)
        with col2:
            global scatter 
            scatter = st.button("Plot scatter chart", key="button3", use_container_width=True)
        chart_displayed = st.session_state.chart_displayed if 'chart_displayed' in st.session_state else False
        if(x_ and y_ and (line or scatter)):
            chart_displayed = True
        st.session_state.x_ = x_
        st.session_state.y_ = y_
        st.session_state.chart_displayed = chart_displayed

def plot_chart(df: DataFrame):
        #faz o gráfico
        chart_displayed = st.session_state.chart_displayed if 'chart_displayed' in st.session_state else False
        x_ = st.session_state.x_ if 'x_' in st.session_state else ''
        y_ = st.session_state.y_ if 'y_' in st.session_state else ''
        if chart_displayed:
            with st.spinner("Please wait..."):
                x_column = x_.upper()
                y_column = y_.upper()
                try:
                    with chart_container(df):
                        #Esse é o gráfico mostrado no site
                        if(line):
                            st.line_chart(df, x=x_column, y=y_column, use_container_width=True)
                        elif(scatter):
                            df2 = df[[x_column, y_column]].copy()
                            c = (alt.Chart(df2).mark_point().encode(x=x_column, y=y_column))
                            st.altair_chart(c, use_container_width=True)
                except:
                    st.error("Invalid Column names.", icon="🚨")
                else:
                    try:
                        #esse é o gráfico do download, feito com matplotlib
                        fig, ax = plt.subplots()
                        if(line):
                            ax.plot(df[x_column], df[y_column])
                        elif(scatter):
                            ax.scatter(df[x_column], df[y_column])
                        ax.set_xlabel(x_column)
                        ax.set_ylabel(y_column)
                        ax.set_title('Line Chart')
                        image_buffer = BytesIO()
                        plt.savefig(image_buffer, format='png')
                        plt.close(fig)


                        image = Image.open(image_buffer)
                        watermark(image, 'data\\LOGO02.png', 20, (180,180), (240,120), (0,0))
                        image = padding(image)

                        imageInfo(image)

                        #Salva a imagem em formato binário para ser baixada usando o download button do streamlit
                        binary_data = BytesIO()
                        image.save(binary_data, format='PNG', compression_level=0) 

                        col1, col2, col3 = st.columns(3)
                        with col2:
                            st.download_button(label="Download Chart Image", data=binary_data, file_name="chart.png", mime="image/png", use_container_width=True)
                    except:
                        st.error("Invalid image for download.", icon="🚨")

def watermark(image, watermark_path, transparency=65, watermark_size=None, position=(0, 0), offset=(0, 0)):
    #Adiciona a marca dagua no gráfico
    watermark = Image.open(watermark_path)    

    if watermark_size:
        watermark = watermark.resize(watermark_size)
    
    if watermark.mode!='RGBA':
        alpha = Image.new('L', watermark.size, 255)
        watermark.putalpha(alpha)

    paste_mask = watermark.split()[3].point(lambda i: i * transparency / 100.)
    paste_position = (position[0] + offset[0], position[1] + offset[1])
    image.paste(watermark, paste_position, mask=paste_mask)

def padding(image):
    #Aumenta o tamanho da imagem para adicionar informaçoes extras
    right = 0
    left = 0
    top = 0
    bottom = 100
    
    width, height = image.size
    
    new_width = width + right + left
    new_height = height + top + bottom
    
    result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
    
    result.paste(image, (left, top))

    return result

def imageInfo(image):
    #Adiciona informações e desenha linhas de separação
    Im = ImageDraw.Draw(image)
    mf = ImageFont.truetype('data\\A101HLVB.ttf', 15)
    Im.line((80, 400, 80, 570), fill=(0, 0, 0), width=1)
    Im.line((576, 400, 576, 570), fill=(0, 0, 0), width=1)
    Im.line((80, 570, 576, 570), fill=(0, 0, 0), width=1)
    Im.line((80, 545, 576, 545), fill=(0, 0, 0), width=1)
    Im.line((80, 520, 576, 520), fill=(0, 0, 0), width=1)
    Im.line((80, 495, 576, 495), fill=(0, 0, 0), width=1)
    Im.line((80, 470, 576, 470), fill=(0, 0, 0), width=1)
    Im.text((85, 475), "Generated at (website url)".upper(),fill=(0, 0, 0), font=mf)
    if "user" in st.session_state:
        Im.text((85, 500), f"User: {st.session_state.user.name}".upper(),fill=(0, 0, 0), font=mf)
    else:
        Im.text((85, 500), "User: John Doe".upper(),fill=(0, 0, 0), font=mf)
    Im.text((85, 525), "Company: Company Name".upper(),fill=(0, 0, 0), font=mf)
    current_dateTime = datetime.now()
    Im.text((85, 550), f"Date: {current_dateTime.year} / {current_dateTime.month:02} / {current_dateTime.day:02}  {current_dateTime.hour:02}:{current_dateTime.minute:02}".upper(),fill=(0, 0, 0), font=mf)