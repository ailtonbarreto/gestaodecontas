#Adicionar Entrada

import streamlit as st
import pandas as pd
import openpyxl as xl

#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",page_title="Adicionar Entrada",initial_sidebar_state='collapsed')
st.title("🟢 Adicionar Entrada",anchor=False)


#----------------------------------------------------------------------------------------
#Dados

df = pd.read_excel("Gestão de contas.xlsx")
pd.to_datetime(df["Data Emissão"])
df["Ano"] = df["Data Emissão"].dt.year
df["Mês"] = df["Data Emissão"].dt.month
df.sort_values("Data Emissão")
df["Ano"].astype(int)
df["Mês"].astype(int)
df['Valor'].astype(float)

def determinar_mês(valor):
    meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez"
    }
    return meses.get(valor)


df["Mês"] = df["Mês"].apply(determinar_mês)
df = df.drop(columns=["Data Emissão"])

#----------------------------------------------------------------------------------------
#Filtros

entrada_fornecedor = st.text_input("Fornecedor")

entrada_notafiscal = st.text_input("Nota Fiscal")

entrada_dataemissao = st.date_input("Data Emissão","today",format= "DD/MM/YYYY")

entrada_datavencimento = st.date_input("Data Vencimento","today",format= "DD/MM/YYYY")
   
entrada_valor = st.number_input("Valor")

entrada_status = st.text_input("Status")


#----------------------------------------------------------------------------------------
#Adicionar a nova linha

if st.button("ADICIONAR"):
    # Abrir o arquivo do Excel
    planilha = xl.load_workbook("Gestão de contas.xlsx")
    planilha = planilha["A Receber"]

    # Criar uma nova linha com os dados inseridos
    nova_linha = [entrada_fornecedor, entrada_notafiscal, entrada_dataemissao, entrada_datavencimento, entrada_valor, entrada_status]
    
    # Adicionar a nova linha à planilha
    planilha.append(nova_linha)

    # Salvar as alterações de volta no arquivo Excel
    planilha.parent.save("Gestão de contas.xlsx")
   
    st.success("Movimentação salva!")

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

