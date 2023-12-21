#Cadastrar Fornecedor

import streamlit as st
import pandas as pd
import openpyxl as xl


st.set_page_config(layout="wide",page_title="Cadastrar Fornecedor",initial_sidebar_state='collapsed')

dffornecedor = pd.read_excel("Gestão de contas.xlsx",sheet_name='Cadastro de Fornecedores')

st.title("📝 Cadastrar Fornecedor",anchor=False)

st.divider()

entrada_fornecedor = st.text_input("Fornecedor")

entrada_categoria = st.selectbox("Categoria",dffornecedor["Categoria"].unique())  


if st.button("ADICIONAR"):
    # Abrir o arquivo do Excel
    planilha = xl.load_workbook("Gestão de contas.xlsx")
    planilha = planilha["Cadastro de Fornecedores"]

    # Criar uma nova linha com os dados inseridos
    nova_linha = [entrada_fornecedor, entrada_categoria]
    
    # Adicionar a nova linha à planilha
    planilha.append(nova_linha)

    # Salvar as alterações de volta no arquivo Excel
    planilha.parent.save("Gestão de contas.xlsx")
   
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
