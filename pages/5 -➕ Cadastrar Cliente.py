#Cadastrar Fornecedor

import streamlit as st
import pandas as pd
import gspread as sg
from gspread import Worksheet



st.set_page_config(layout="wide",page_title="Cadastrar Cliente",initial_sidebar_state='collapsed',page_icon='📊')
st.sidebar.link_button("Ver Planilha","https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

#----------------------------------------------------------------------------------------------------------------------------
#Tratamento e carregamento

gc = sg.service_account("gestao.json")
url = 'https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing'
sh = gc.open_by_url(url)
ws = sh.get_worksheet(3)
planilha = ws.get_all_values()
dffornecedor = pd.DataFrame(planilha[1:], columns=planilha[0])

#----------------------------------------------------------------------------------------------------------------------------
#Cadastrar Fornecedor
st.title("📝 Cadastrar Cliente",anchor=False)

st.divider()

entrada_cliente = st.text_input("Cliente")


if st.button("ADICIONAR"):
    # Abrir o arquivo do Excel
    ws: Worksheet = sh.get_worksheet(3)
    novo_cliente = [entrada_cliente]
    # Criar uma nova linha com os dados inseridos
    ws.append_row(novo_cliente)
   
    st.success("Cliente Cadastrado!")
st.divider()

st.table(dffornecedor)
#------------------------------------------------------------------------------------------
#Esconder streamlit menus


framegraficos = """
    <style>
    [class="styles_stateContainer__CelYF""]
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

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
