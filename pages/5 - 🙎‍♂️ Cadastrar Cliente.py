#Cadastrar Fornecedor

import streamlit as st
import pandas as pd
import openpyxl as xl


st.set_page_config(layout="wide",page_title="Cadastrar Cliente",initial_sidebar_state='collapsed',page_icon='✅')

dfcliente = pd.read_excel("Gestão de contas.xlsx",sheet_name='Cadastro de Clientes')

st.title("📝 Cadastrar Cliente",anchor=False)

st.divider()

entrada_cliente = st.text_input("Cliente")


if st.button("ADICIONAR"):
    # Abrir o arquivo do Excel
    planilha = xl.load_workbook("Gestão de contas.xlsx")
    planilha = planilha["Cadastro de Clientes"]

    # Criar uma nova linha com os dados inseridos
    nova_linha = [entrada_cliente]
    
    # Adicionar a nova linha à planilha
    planilha.append(nova_linha)

    # Salvar as alterações de volta no arquivo Excel
    planilha.parent.save("Gestão de contas.xlsx")
   
    st.success("Cliente Cadastrado com Sucesso!")
st.divider()

st.table(dfcliente)
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
