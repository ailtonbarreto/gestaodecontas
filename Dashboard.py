#----------------------------------------------------------------------------------------
#Dashboard Gestão de contas

import streamlit as st
import pandas as pd
import plotly.express as px
import openpyxl as xl

#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",initial_sidebar_state='collapsed',page_icon='✅')
#----------------------------------------------------------------------------------------
#Layout em duas colunas
col1,col2,col3,col4,col5 = st.columns([3,2,2,2,1])
col7,col8 = st.columns(2)
col9,col10 = st.columns([100,1])

#----------------------------------------------------------------------------------------
#Dados saidas

dfsaida1 = xl.load_workbook('Gestão de contas.xlsx')
dfsaida = dfsaida1['A Pagar'].values
df1 = pd.DataFrame(dfsaida).drop(columns=[1,2,4])
dfsaidas = df1.rename(columns={0:'Data emissão',3:'Valor',5:'Tipo'})
dfsaidas = dfsaidas.drop(dfsaidas.index[0])

#----------------------------------------------------------------------------------------
#Dados entradas

dfentrada = xl.load_workbook('Gestão de contas.xlsx')
dfentrada = dfentrada['A Receber'].values
df2 = pd.DataFrame(dfentrada).drop(columns=[0,1,3,5])
dfentradas = df2.rename(columns={2:'Data emissão',4:'Valor',6:"Tipo"})
dfentradas = dfentradas.drop(dfentradas.index[0])

#----------------------------------------------------------------------------------------
#dataframes concatenados para analise de entradas e saídas

df = pd.concat([dfsaidas,dfentradas]).reset_index(drop=True)

df["Ano"] = pd.to_datetime(df['Data emissão']).dt.year
df["Mês"] = pd.to_datetime(df['Data emissão']).dt.month
df["Valor"].astype(float)

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
        10: "Out",
        11: "Nov",
        12: "Dez"
    }
    return meses.get(valor)

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
df = df.drop(columns=["Data emissão"])
df['Ordem_Mês'] = df['Mês'].map(classificar_meses)
df = df.sort_values(by='Ordem_Mês',ascending = True).drop(columns=['Ordem_Mês'])
df = df.sort_values(by='Ano',ascending = True)
#----------------------------------------------------------------------------------------
#filtro mensal

selectboxmeses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']

#----------------------------------------------------------------------------------------
#Filtros/Layout

with col1:
    # st.title("Gestão à Vista",anchor=False)
    st.image('money-flow.png',width=200)
   
with col5:
    filtro_ano = st.selectbox("Ano", df["Ano"].unique())  
    filtro_mes = st.selectbox("Mês",selectboxmeses) 

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


df_filtrado4 = df.loc[(df["Ano"] == filtro_ano) & (df["Tipo"] == "ENTRADA") & (df["Mês"] == filtro_mes)]

#----------------------------------------------------------------------------------------
#Dataframe contas a pagar

dfgrafico = pd.read_excel('Gestão de contas.xlsx',sheet_name="A Pagar")
dfgrafico['Ano'] = dfgrafico['Data Emissão'].dt.year
dfgrafico['Mês'] = dfgrafico['Data Emissão'].dt.month
dfgrafico["Mês"] = dfgrafico["Mês"].apply(determinar_mês)
dfgrafico = dfgrafico.groupby(["CATEGORIA", "Ano","Mês"])["Valor"].sum().reset_index()

dfgrafico = dfgrafico.query('Ano == @filtro_ano & Mês == @filtro_mes')

dfgrafico = dfgrafico.sort_values(by="Valor",ascending=True)

#----------------------------------------------------------------------------------------
#Gráficos

grafico_Rosca = px.pie(df_filtrado1,names="Tipo",color='Tipo',category_orders={'Tipo':['ENTRADA','SAÍDA']},
        values="Valor",color_discrete_sequence=["#06d6a0","#941b0c"],title='Entradas VS Saídas')
grafico_Rosca.update_traces(showlegend=False)


grafico_colunas = px.bar(df_filtrado3,x="Mês",y="Valor",color="Tipo",
        barmode="group",title=f'Entradas e Saídas de {filtro_ano}',category_orders={'Tipo':['ENTRADA','SAÍDA']},
        color_discrete_sequence=["#06d6a0","#941b0c"])
grafico_colunas.update_yaxes(showgrid=False)
grafico_colunas.update_traces(showlegend=False)

grafico_barras = px.bar(dfgrafico,x="Valor",y="CATEGORIA",orientation="h",title=f"Despesas de {filtro_mes} de {filtro_ano}",color_discrete_sequence=["#941b0c"])

#----------------------------------------------------------------------------------------
#Layout gráficos

with col2:
    st.subheader("Entradas",anchor=False)
    st.metric('',f'R$ {round(df_filtrado4["Valor"].sum(),2):,.2f}')
with col3:
    st.subheader("Saídas",anchor=False)
    st.metric("",f'R$ {round(df_filtrado2["Valor"].sum(),2):,.2f}')
with col4:
    st.subheader("Saldo",anchor=False)
    st.metric("",f'R$ {round(df_filtrado4["Valor"].sum()-df_filtrado2["Valor"].sum(),2):,.2f}')
with col7:
    st.divider()
    st.plotly_chart(grafico_Rosca,use_container_width=True) 
with col8:
    st.divider()
    st.plotly_chart(grafico_barras,use_container_width=True)
with col9:
    st.divider()
    st.plotly_chart(grafico_colunas,use_container_width=True)
    st.divider()


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
