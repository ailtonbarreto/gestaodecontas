#----------------------------------------------------------------------------------------
#Adicionar Entrada

import streamlit as st
import pandas as pd
import gspread as sg
from gspread import Worksheet


#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",page_title="Adicionar Entrada",initial_sidebar_state='collapsed',page_icon='📊')


tab1, tab2, tab3 = st.tabs(['Adicionar Entrada','Excluir Entrada','Editar uma Entrada'])

#----------------------------------------------------------------------------------------
#Dados Entradas

gc = sg.service_account("gestao.json")
url = 'https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing'
sh = gc.open_by_url(url)
ws = sh.get_worksheet(0)
planilha = ws.get_all_values()
df = pd.DataFrame(planilha[1:], columns=planilha[0])

df['Data'] = pd.to_datetime(df["Data Vencimento"])
df["Ano"] = df["Data"].dt.year
df["Mês"] = df["Data"].dt.month
df.sort_values("Data", inplace=True)
df["Ano"] = df["Ano"].astype(int)
df["Mês"] = df["Mês"].astype(int)
df['Valor'] = df['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)

#----------------------------------------------------------------------------------------

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
#Adicionar Entrada

with tab1:

    st.title("🟢 Adicionar Entrada",anchor=False)
    planilhaclientes = gc.open_by_url(url)
    dfselect = sh.get_worksheet(3)
    dfselect = ws.get_all_values()
    dfselect = pd.DataFrame(dfselect[1:], columns=dfselect[0])
    
    entrada_cliente = st.selectbox("Clientes",dfselect['Cliente'].unique())

    entrada_notafiscal = st.text_input("Nota Fiscal")

    entrada_dataemissao = st.date_input("Data Emissão","today",format= "DD/MM/YYYY")

    entrada_datavencimento = st.date_input("Data Vencimento","today",format= "DD/MM/YYYY")
   
    entrada_valor = st.text_input("Valor",value="0,00")

    entrada_status = st.selectbox("Status",["A RECEBER","RECEBIDO"])

    if st.button("ADICIONAR"):
        ws: Worksheet = sh.get_worksheet(0)
        entrada_dataemissao = entrada_dataemissao.strftime("%Y-%m-%d")
        entrada_datavencimento = entrada_datavencimento.strftime("%Y-%m-%d")
    # Criar uma nova linha com os dados inseridos
        nova_linha = [entrada_cliente, entrada_notafiscal, entrada_dataemissao, entrada_datavencimento, entrada_valor, entrada_status,"ENTRADA"]
    
    # Adicionar a nova linha à planilha
        ws.append_row(nova_linha)
           
        st.success("Movimentação salva!")
    st.table(dfselect)

#----------------------------------------------------------------------------------------
# Excluir Entrada
with tab2:
    st.title("🟢 Excluir Entrada",anchor=False)
    dfexcluir = df
    filtro_ano = st.selectbox("Ano",dfexcluir["Ano"].unique())
    filtro_mes = st.selectbox("Mês",dfexcluir["Mês"].unique())

    filtro_cliente = st.selectbox('Cliente',dfselect["Cliente"].unique())
    linha = st.number_input("Excluir linha",format="%.0f")

    dfexcluir = dfexcluir.query('Ano == @filtro_ano & Mês == @filtro_mes & Cliente == @filtro_cliente')

    if st.button("EXCLUIR ENTRADA"):
        ws1: Worksheet = sh.get_worksheet(0)
       
        ws1.delete_rows(int(linha) + 2)
    
        st.success("Entrada Excluída Com Sucesso!")

    
    st.table(dfexcluir)
#----------------------------------------------------------------------------------------
#Editar Entrada

with tab3:
    st.title("🟢 Editar Entrada",anchor=False)

    dfeditarentrada = df
    
    #Dados da linha editada
    filtro_y = st.selectbox('Ano da Movimentação',dfeditarentrada["Ano"].unique())
    filtro_m = st.selectbox('Mês da Movimentação',dfeditarentrada["Mês"].unique())
    filtro_c = st.selectbox('Buscar Cliente',dfeditarentrada["Cliente"].unique())
    filtro_index = st.number_input("Linha a Editar",format="%.0f")
    editar_status = st.selectbox('Novo Status',["A RECEBER","RECIBIDO"])
    
    dfeditarentrada = df.query('Ano == @filtro_y & Mês == @filtro_m & Cliente == @filtro_c')

    linhaeditada = filtro_index + 2

    coluna = 6



    if st.button("SALVAR EDIÇÃO"):
        ws2: Worksheet = sh.get_worksheet(0)
        
        ws2.update_cell(linhaeditada, coluna, editar_status)
       
    
        st.success("Edição salva!")

    dfeditarentrada["Valor"] = dfeditarentrada["Valor"].apply(lambda x: f'R$ {x:,.2f}')
    
    st.table(dfeditarentrada)


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

