#----------------------------------------------------------------------------------------
#Dashboard Gestao de contas

import streamlit as st
import pandas as pd
import plotly.express as px
import gspread as sg
import datetime as dt



#----------------------------------------------------------------------------------------
#exibicao de dados

st.set_page_config(layout="wide",initial_sidebar_state='collapsed',page_icon='📊',page_title="Gestão À Vista")
st.sidebar.link_button("Ver Planilha","https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

#----------------------------------------------------------------------------------------
#Layout em duas colunas

st.title("📊 Gestão à Vista",anchor=False)
st.divider()
col2,col3,col4,col5,col6 = st.columns([2,2,2,1,1])
col7,col8 = st.columns(2)
col9, = st.columns(1)
col10, = st.columns(1)


#----------------------------------------------------------------------------------------
#Dados 

urlsaida = "https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/pub?gid=167245010&single=true&output=csv"
urlentrada = "https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/pub?gid=1081596630&single=true&output=csv"
urlsaida2 = "https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/pub?gid=167245010&single=true&output=csv"

@st.cache_data
def get_datasaida():
    planilha = pd.read_csv(urlsaida)
    return planilha


@st.cache_data
def get_dataentrada(urlentrada):
    planilha1 = pd.read_csv(urlentrada)
    return planilha1

@st.cache_data
def get_saida2(urlsaida2):
    dfgrafico = dfgrafico = pd.read_csv(urlsaida2)
    return dfgrafico


dfgrafico = get_saida2(urlsaida2)

dfsaida = get_datasaida(urlsaida)
dfsaida['Data'] = pd.to_datetime(dfsaida["Data Emissão"])
dfsaida["Ano"] = dfsaida["Data"].dt.year
dfsaida["Mês"] = dfsaida["Data"].dt.month
dfsaida.sort_values("Data", inplace=True)
dfsaida["Ano"] = dfsaida["Ano"].astype(int)
dfsaida["Mês"] = dfsaida["Mês"].astype(int)
dfsaida['Valor'] = dfsaida['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)
dfsaida = pd.DataFrame(dfsaida).drop(columns=["CATEGORIA"])


dfentrada = get_dataentrada(urlentrada)
dfentrada['Data'] = pd.to_datetime(dfentrada["Data Vencimento"])
dfentrada['Fornecedor'] = dfentrada["Cliente"]
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

#----------------------------------------------------------------------------------------
#funcao para definir situacao das contas

def definir_situacao(status, data):
    
    if status in ['PAGO', 'RECEBIDO']:
        return 'OK'
    elif status in ['A PAGAR', 'A RECEBER'] and pd.to_datetime(data).date() > dt.date.today():
        return 'EM DIA'
    elif status in ['A PAGAR', 'A RECEBER'] and pd.to_datetime(data).date() == dt.date.today():
        return 'VENCE HOJE'
    else:
        return 'ATRASADO'


df['Situacao'] = df.apply(lambda row: definir_situacao(row['Status'], row['Data']), axis=1)
df.sort_values(by="Data",ascending=True)



df["Ano"] = pd.to_datetime(df['Data']).dt.year
df["Mês"] = pd.to_datetime(df['Data']).dt.month
df["Data"] = df["Data"].dt.strftime('%d/%m/%Y')


#----------------------------------------------------------------------------------------
#funcao para classificar meses

def determinar_mes(valor):
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
#dicionario para classificar meses

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

df["Mês"] = df["Mês"].apply(determinar_mes)
df = df.drop(columns=["Data Emissão"])
df['Ordem_Mês'] = df['Mês'].map(classificar_meses)
df = df.sort_values(by='Ordem_Mês',ascending = True).drop(columns=['Ordem_Mês'])
df = df.sort_values("Ano",ascending=False)

#----------------------------------------------------------------------------------------
#fixar mes atual no filtro

today = dt.date.today()


mes = today.month

if mes == 1:
    mes_atual = "Jan"
elif mes == 2:
    mes_atual = "Fev"
elif mes == 3:
    mes_atual = "Mar"
elif mes == 4:
    mes_atual = "Abr"
elif mes == 5:
    mes_atual = "Mai"
elif mes == 6:
    mes_atual = "Jun"
elif mes ==7:    
    mes_atual = "Jul"
elif mes == 8:    
    mes_atual = "Ago"
elif mes == 9:    
   mes_atual =  "Set"
elif mes == 10:    
   mes_atual =  "Out"
elif mes == 11:    
    mes_atual = "Nov"
else:
    "Dez"


#----------------------------------------------------------------------------------------
#Filtros/Layout


    
   
with col5:
    filtro_ano = st.selectbox("Ano", df["Ano"].unique())  
    
with col6:
     filtro_mes = st.selectbox("Mês", meses,index=meses.index(mes_atual)) 
with col10:
    st.title("Histórico de Movimentações 📅",anchor=False)
    filtro_ano_movi = st.selectbox("Selecione um Ano", df["Ano"].unique())  
    
#----------------------------------------------------------------------------------------
#Dataframes filtrados

df_filtrado1 = df.loc[(df["Ano"] == filtro_ano) & (df["Mês"] == filtro_mes)]
df_filtrado1 = df_filtrado1.drop(columns=["Ano","Mês"])
df_filtrado1 = df_filtrado1.sort_values("Data",ascending=True)

df_filtrado2 = df.loc[(df["Ano"] == filtro_ano) & (df["Tipo"] == "SAÍDA") & (df["Mês"] == filtro_mes)]
df_filtrado2 = df_filtrado2.groupby(['Tipo','Mês'])['Valor'].sum().reset_index()
df_filtrado2 = df_filtrado2.sort_values('Valor')

df_filtrado3 = df.loc[(df["Ano"] == filtro_ano_movi)]
df_filtrado3 = df_filtrado3.groupby(["Tipo","Mês"])["Valor"].sum().reset_index()
df_filtrado3['Ordem_Mês'] = df_filtrado3['Mês'].map(classificar_meses)
df_filtrado3 = df_filtrado3.sort_values(by='Ordem_Mês',ascending = True).drop(columns=['Ordem_Mês'])

df_filtrado4 = df.query('Ano == @filtro_ano & Mês == @filtro_mes & Tipo == "ENTRADA"')

#----------------------------------------------------------------------------------------
#Graficos

grafico_Rosca = px.pie(df_filtrado1,names="Tipo",color='Tipo',category_orders={'Tipo':['SAÍDA','ENTRADA']},
        values="Valor",color_discrete_sequence=["#941b0c","#06d6a0"],title='Entradas VS Saídas')
grafico_Rosca.update_traces(showlegend=False,textfont=dict(size=15,color='#ffffff'))


grafico_colunas = px.bar(df_filtrado3,x="Mês",y="Valor",color="Tipo",
        barmode="group",title=f'Entradas e Saídas de {filtro_ano_movi}',category_orders={'Tipo':['SAÍDA','ENTRADA']},
        color_discrete_sequence=["#941b0c","#06d6a0"])
grafico_colunas.update_yaxes(showgrid=False)
grafico_colunas.update_traces(showlegend=False)
grafico_colunas.update_yaxes(showgrid=False,visible=True,title="")
grafico_colunas.layout.xaxis.fixedrange = True
grafico_colunas.layout.yaxis.fixedrange = True
#----------------------------------------------------------------------------------------





dfgrafico['Data'] = pd.to_datetime(dfgrafico["Data Emissão"])
dfgrafico['Ano'] = dfgrafico['Data'].dt.year
dfgrafico['Mês'] = dfgrafico['Data'].dt.month
dfgrafico["Mês"] = dfgrafico["Mês"].apply(determinar_mes)
dfgrafico = dfgrafico.drop(columns=["Data Emissão","Data"])
dfgrafico['Valor'] = dfgrafico['Valor'].astype(str)
dfgrafico['Valor'] = dfgrafico['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)
dfgrafico = dfgrafico.groupby(["CATEGORIA", "Ano","Mês","Status"])["Valor"].sum().reset_index()
dfgrafico = dfgrafico.query('Ano == @filtro_ano & Mês == @filtro_mes')
dfgrafico = dfgrafico.sort_values(by="Valor",ascending=True)

grafico_barras = px.bar(dfgrafico,x="Valor",y="CATEGORIA",text=dfgrafico["Valor"].apply(lambda x: f'R$ {x:,.2f}'),
        orientation="h",category_orders={'Status':['PAGO','A PAGAR']},
        title=f"Despesas de {filtro_mes} de {filtro_ano}",color="Status",barmode="stack",
        color_discrete_sequence=["#0aefff","#ee9b00"])
grafico_barras.update_yaxes(showgrid=False,visible=True,title="")
grafico_barras.update_xaxes(showgrid=False,visible=False,title="")
grafico_barras.layout.xaxis.fixedrange = True
grafico_barras.layout.yaxis.fixedrange = True
grafico_barras.update_layout(showlegend=False)
grafico_barras.update_traces(textfont=dict(size=15,color='#ffffff'),textposition="outside")


#----------------------------------------------------------------------------------------
#definir icone
 
if df_filtrado4["Valor"].sum()-df_filtrado2["Valor"].sum() >= 0:
        icon = "🔼"
else:
    icon = "🔽"
    
#----------------------------------------------------------------------------------------
#formatar moeda

df_filtrado1["Valor"] = df_filtrado1["Valor"].apply(lambda x: f'R$ {x:,.2f}')



#----------------------------------------------------------------------------------------
#Layout graficos

with col2:
    st.metric("Entrada",f'🟢 R$ {round(df_filtrado4["Valor"].sum(),2):,.2f}')
with col3:
    st.metric("Saídas",f'🔴 R$ {round(df_filtrado2["Valor"].sum(),2):,.2f}')
with col4:
    st.metric("Saldo do Mês",f'{icon} R$ {round(df_filtrado4["Valor"].sum()-df_filtrado2["Valor"].sum(),2):,.2f}')
with col7:
    st.plotly_chart(grafico_Rosca,use_container_width=True) 
with col8:
    st.plotly_chart(grafico_barras,use_container_width=True)
with col9:
    st.subheader(f"Movimentações de {filtro_mes} de {filtro_ano}",anchor=False) 
    filtro_mov = st.selectbox("Tipo",["ENTRADA","SAÍDA"])
    df_movi = df_filtrado1.query('Tipo == @filtro_mov')
    st.dataframe(df_movi,use_container_width=True,hide_index=True)

with col10:
    st.plotly_chart(grafico_colunas,use_container_width=True)
#------------------------------------------------------------------------------------------
#CSS

framegraficos = """
    <style>
    [data-testid="column"]
    {
    border-radius: 15px;
    background-color: #2F3035;
    padding: 10px;
    opacity: 80%;
    color: white;
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
    [class="modebar-container"]
    {
    visibility: hidden;
    }
    </style>
"""


st.markdown(detalhes,unsafe_allow_html=True)

alinhartitulo = """
    <style>
    [id="a7776087"]
    {
    text-align: center;
    }
    </style>
"""
st.markdown(alinhartitulo,unsafe_allow_html=True)


sumirfundo = """
    <style>
    [class="st-emotion-cache-17xod8c e1f1d6gn3"]
    {
    background: none;
    }
    </style>
"""
st.markdown(sumirfundo,unsafe_allow_html=True)




hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)




