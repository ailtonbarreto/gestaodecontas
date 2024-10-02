#Cadastrar Fornecedor

import streamlit as st
import pandas as pd
import gspread as sg
from gspread import Worksheet



st.set_page_config(layout="wide",page_title="Cadastrar Fornecedor",initial_sidebar_state='collapsed',page_icon='📊')
# st.sidebar.link_button("Ver Planilha","https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

#----------------------------------------------------------------------------------------------------------------------------
#Tratamento e carregamento

gc = sg.service_account("gestao.json")
url = 'https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing'
sh = gc.open_by_url(url)
ws = sh.get_worksheet(2)
planilha = ws.get_all_values()
dffornecedor = pd.DataFrame(planilha[1:], columns=planilha[0])



#----------------------------------------------------------------------------------------------------------------------------
#Cadastrar Fornecedor
st.title("📝 Cadastrar Fornecedor",anchor=False)

st.divider()

entrada_fornecedor = st.text_input("Fornecedor")

entrada_categoria = st.selectbox("Categoria",dffornecedor["Categoria"].unique())  


if st.button("ADICIONAR"):
    # Abrir o arquivo do Excel
    ws: Worksheet = sh.get_worksheet(2)
    novo_cadastro = [entrada_fornecedor,entrada_categoria]
    # Criar uma nova linha com os dados inseridos
    ws.append_row(novo_cadastro)
   
    st.success("Fornecedor Cadastrado!")
st.divider()

st.table(dffornecedor)
#------------------------------------------------------------------------------------------
#Esconder streamlit menus

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

framegraficos = """
    <style>
    [data-testid="stColumn"]
    {
    border-radius: 15px;
    background-color: #2F3035;
    padding: 20px;
    opacity: 80%;
    color: white;
    
    }
    </style>
"""
st.markdown(framegraficos,unsafe_allow_html=True)

desativartelacheia = """
    <style>
    [data-testid="StyledFullScreenButton"]
    {
    visibility: hidden;
    }
    </style>
"""
st.markdown(desativartelacheia,unsafe_allow_html=True)