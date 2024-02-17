#----------------------------------------------------------------------------------------
#Dashboard Gestão de contas

import streamlit as st
import pandas as pd
import plotly.express as px
import gspread as sg


#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",initial_sidebar_state='collapsed',page_icon='📊')
st.sidebar.link_button("Ver Planilha","https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

#----------------------------------------------------------------------------------------
#Layout em duas colunas

col1,col2,col3,col4,col5,col6 = st.columns([3,2,2,2,1,1])
col7,col8 = st.columns(2)
col9,col10 = st.columns([100,1])


#----------------------------------------------------------------------------------------
#Dados saidas

gc = sg.service_account("gestao.json")
url = 'https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing'
sh = gc.open_by_url(url)
ws = sh.get_worksheet(1)
planilha = ws.get_all_values()
dfsaida = pd.DataFrame(planilha[1:], columns=planilha[0])

dfsaida['Data'] = pd.to_datetime(dfsaida["Data Emissão"])
dfsaida["Ano"] = dfsaida["Data"].dt.year
dfsaida["Mês"] = dfsaida["Data"].dt.month
dfsaida.sort_values("Data", inplace=True)
dfsaida["Ano"] = dfsaida["Ano"].astype(int)
dfsaida["Mês"] = dfsaida["Mês"].astype(int)
dfsaida['Valor'] = dfsaida['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)
dfsaida = pd.DataFrame(dfsaida).drop(columns=["Fornecedor","CATEGORIA"])

#----------------------------------------------------------------------------------------
#Dados entradas

ws1 = sh.get_worksheet(0)
planilha1 = ws1.get_all_values()
dfentrada = pd.DataFrame(planilha1[1:], columns=planilha1[0])
dfentrada['Data'] = pd.to_datetime(dfentrada["Data Vencimento"])
dfentrada = pd.DataFrame(dfentrada).drop(columns=["Cliente","Nota Fiscal","Data Vencimento"])
dfentrada["Ano"] = dfentrada["Data"].dt.year
dfentrada["Mês"] = dfentrada["Data"].dt.month
dfentrada.sort_values("Data", inplace=True)
dfentrada["Ano"] = dfentrada["Ano"].astype(int)
dfentrada["Mês"] = dfentrada["Mês"].astype(int)
dfentrada['Valor'] = dfentrada['Valor'].astype(str)
dfentrada['Valor'] = dfentrada['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)

#----------------------------------------------------------------------------------------
#dataframes concatenados para analise de entradas e saídas

df = pd.concat([dfsaida,dfentrada]).reset_index(drop=True)
df["Ano"] = pd.to_datetime(df['Data']).dt.year
df["Mês"] = pd.to_datetime(df['Data']).dt.month

#----------------------------------------------------------------------------------------
#funcão para classificar meses

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
        10:"Out",
        11:"Nov",
        12:"Dez"
    }
    return meses.get(valor)
#----------------------------------------------------------------------------------------
#Meses

meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']


#----------------------------------------------------------------------------------------
#dicionário para classificar meses

classificar_meses ={
    'Jan': 1,
    'Fev': 2,
    'Mar': 3,
    'Abr': 4,
    'Mai': 5,
    'Jun': 6,
    'Jul': 7,
    'Ago': 8,
    'Set': 9,
    'Out': 10,
    'Nov': 11,
    'Dez': 12
        }

df["Mês"] = df["Mês"].apply(determinar_mês)
df = df.drop(columns=["Data Emissão"])
df['Ordem_Mês'] = df['Mês'].map(classificar_meses)
df = df.sort_values(by='Ordem_Mês',ascending = True).drop(columns=['Ordem_Mês',"Data"])
df = df.sort_values("Ano",ascending=False)

#----------------------------------------------------------------------------------------
#Filtros/Layout

with col1:
    st.title("Gestão à Vista",anchor=False)
   
with col5:
    filtro_ano = st.selectbox("Ano", df["Ano"].unique())  
    
with col6:
     filtro_mes = st.selectbox("Mês", meses) 

#----------------------------------------------------------------------------------------
#Dataframes filtrados

df_filtrado1 = df.loc[(df["Ano"] == filtro_ano) & (df["Mês"] == filtro_mes)]

df_filtrado2 = df.loc[(df["Ano"] == filtro_ano) & (df["Tipo"] == "SAÍDA") & (df["Mês"] == filtro_mes)]
df_filtrado2 = df_filtrado2.groupby(['Tipo','Mês'])['Valor'].sum().reset_index()
df_filtrado2 = df_filtrado2.sort_values('Valor')

df_filtrado3 = df.loc[(df["Ano"] == filtro_ano)]
df_filtrado3 = df_filtrado3.groupby(["Tipo","Mês"])["Valor"].sum().reset_index()
df_filtrado3['Ordem_Mês'] = df_filtrado3['Mês'].map(classificar_meses)
df_filtrado3 = df_filtrado3.sort_values(by='Ordem_Mês',ascending = True).drop(columns=['Ordem_Mês'])

df_filtrado4 = df.query('Ano == @filtro_ano & Mês == @filtro_mes & Tipo == "ENTRADA"')

#----------------------------------------------------------------------------------------
#Gráficos

grafico_Rosca = px.pie(df_filtrado1,names="Tipo",color='Tipo',category_orders={'Tipo':['SAÍDA','ENTRADA']},
        values="Valor",color_discrete_sequence=["#941b0c","#06d6a0"],title='Entradas VS Saídas')
grafico_Rosca.update_traces(showlegend=False)


grafico_colunas = px.bar(df_filtrado3,x="Mês",y="Valor",color="Tipo",
        barmode="group",title=f'Entradas e Saídas de {filtro_ano}',category_orders={'Tipo':['SAÍDA','ENTRADA']},
        color_discrete_sequence=["#941b0c","#06d6a0"])
grafico_colunas.update_yaxes(showgrid=False)
grafico_colunas.update_traces(showlegend=False)
#----------------------------------------------------------------------------------------

gc = sg.service_account("gestao.json")
url = 'https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing'
sheet = gc.open_by_url(url)
dfgrafico = sh.get_worksheet(1)
dfgrafico = ws.get_all_values()
dfgrafico = pd.DataFrame(planilha[1:], columns=planilha[0])

dfgrafico['Data'] = pd.to_datetime(dfgrafico["Data Emissão"])
dfgrafico['Ano'] = dfgrafico['Data'].dt.year
dfgrafico['Mês'] = dfgrafico['Data'].dt.month
dfgrafico["Mês"] = dfgrafico["Mês"].apply(determinar_mês)
dfgrafico = dfgrafico.drop(columns=["Data Emissão","Data"])
dfgrafico['Valor'] = dfgrafico['Valor'].astype(str)
dfgrafico['Valor'] = dfgrafico['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)
dfgrafico = dfgrafico.groupby(["CATEGORIA", "Ano","Mês","Status"])["Valor"].sum().reset_index()
dfgrafico = dfgrafico.query('Ano == @filtro_ano & Mês == @filtro_mes')
dfgrafico = dfgrafico.sort_values(by="Valor",ascending=True)

grafico_barras = px.bar(dfgrafico,x="Valor",y="CATEGORIA",
        orientation="h",category_orders={'Status':['PAGO','A PAGAR']},
        title=f"Despesas de {filtro_mes} de {filtro_ano}",color="Status",barmode="stack",
        color_discrete_sequence=["#0aefff","#ee9b00"])

#----------------------------------------------------------------------------------------
#Layout gráficos

with col2:
    st.metric("Entrada",f'R$ {round(df_filtrado4["Valor"].sum(),2):,.2f}')
with col3:
    st.metric("Saídas",f'R$ {round(df_filtrado2["Valor"].sum(),2):,.2f}')
with col4:
    st.metric("Saldo do Mês",f'R$ {round(df_filtrado4["Valor"].sum()-df_filtrado2["Valor"].sum(),2):,.2f}')
with col7:
    st.plotly_chart(grafico_Rosca,use_container_width=True) 
with col8:
    st.plotly_chart(grafico_barras,use_container_width=True)
with col9:
    st.plotly_chart(grafico_colunas,use_container_width=True)   
#------------------------------------------------------------------------------------------
#Estilizacao

borda_graficos = """
    <style>
    [class="user-select-none svg-container"]
    {
    background-color: white;
    border-radius: 20px;
    }
    </style>
"""
st.markdown(borda_graficos,unsafe_allow_html=True)


framegraficos = """
    <style>
    [data-testid="column"]
    {
    border-radius: 15px;
    background-color: black;
    border-color: white;
    padding: 20px;
    
    }
    </style>
"""
st.markdown(framegraficos,unsafe_allow_html=True)

divesconder = """
    <style>
    [class="st-emotion-cache-acqtcz e1f1d6gn3"]
    {
    visibility: hidden;
    }
    </style>
"""
st.markdown(divesconder,unsafe_allow_html=True)

desativartelacheia = """
    <style>
    [data-testid="StyledFullScreenButton"]
    {
    visibility: hidden;
    }
    </style>
"""
st.markdown(desativartelacheia,unsafe_allow_html=True)



detalhes = """
    <style>
    [id="modebar-507362"]
    {
    visibility: hidden;
    }
    </style>
"""
st.markdown(detalhes,unsafe_allow_html=True)