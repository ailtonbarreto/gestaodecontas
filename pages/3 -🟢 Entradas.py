#----------------------------------------------------------------------------------------
#Adicionar Entrada

import streamlit as st
import pandas as pd
import gspread as sg
from gspread import Worksheet
import datetime as dt


#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",page_title="Adicionar Entrada",initial_sidebar_state='collapsed',page_icon='📊')
st.sidebar.link_button("Ver Planilha","https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

tab1, tab2, tab3, tab4 = st.tabs(['Adicionar Entrada','Excluir Entrada','Editar uma Entrada','Recebimentos em Aberto'])

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
#funcão para definir situacao das contas

def definir_situacao(status, data):
    
    if status in ['PAGO', 'RECEBIDO']:
        return 'OK'
    elif status in ['A PAGAR', 'A RECEBER'] and pd.to_datetime(data).date() > dt.date.today():
        return 'EM DIA'
    elif status in ['A PAGAR', 'A RECEBER'] and pd.to_datetime(data).date() == dt.date.today():
        return 'VENCE HOJE'
    else:
        return 'ATRASADO'


df['Situacao'] = df.apply(lambda row: definir_situacao(row['Status'], row['Data Vencimento']), axis=1)
df.sort_values(by="Data",ascending=True)


#----------------------------------------------------------------------------------------
#Meses

meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']

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
#fixar mes atual nos filtros

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
#Adicionar Entrada

with tab1:

    st.title("🟢 Adicionar Entrada",anchor=False)
    planilhaclientes = gc.open_by_url(url)
    dfselect = planilhaclientes.get_worksheet(3)
    dfselect = dfselect.get_all_values()
    dfselect = pd.DataFrame(dfselect[1:], columns=dfselect[0])
    
    entrada_cliente = st.selectbox("Clientes",dfselect['Cliente'].unique())

    entrada_notafiscal = st.text_input("Nota Fiscal")

    entrada_dataemissao = st.date_input("Data Emissão","today",format= "DD/MM/YYYY")

    entrada_datavencimento = st.date_input("Data Vencimento","today",format= "DD/MM/YYYY")
   
    entrada_valor = st.number_input("Valor", value=None, format="%.2f")


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
    

#----------------------------------------------------------------------------------------
# Excluir Entrada
with tab2:
    st.title("🟢 Excluir Entrada",anchor=False)
    dfexcluir = df.sort_values("Ano",ascending=False)
    filtro_ano = st.selectbox("Ano",dfexcluir["Ano"].unique())
    filtro_mes = st.selectbox("Mês",meses,index=meses.index(mes_atual))

    filtro_cliente = st.selectbox('Cliente',dfselect["Cliente"].unique())

    opcoes = dfexcluir.query('Ano == @filtro_ano & Mês == @filtro_mes & Cliente == @filtro_cliente')
    
    opcoes = opcoes.drop(columns=["Data","Ano","Mês"])
    
    opcoesdelete = opcoes.index.tolist()
    col1, col2 = st.columns([1, 10])
    
    with col1:
        linha1 = st.selectbox("Selecionar linha", opcoesdelete)
    
    
    
    with col2:
        st.table(opcoes)
        if st.button("EXCLUIR ENTRADA"):
            
            ws1: Worksheet = sh.get_worksheet(0)
        
            ws1.delete_rows(int(linha1) + 2)
        
            st.success("Entrada Excluída Com Sucesso!")

        opcoes["Valor"] = opcoes["Valor"].apply(lambda x: f'R$ {x:,.2f}')
        opcoes["Data Vencimento"] =pd.to_datetime(opcoes["Data Vencimento"]).dt.strftime('%d/%m/%Y') 
        
    

#----------------------------------------------------------------------------------------
#Editar Entrada

with tab3:
    st.title("🟢 Editar Entrada",anchor=False)

    dfeditarentrada = df.sort_values("Ano",ascending=False)
    
    #Dados da linha editada
    filtro_y = st.selectbox('Ano da Movimentação',dfeditarentrada["Ano"].unique())
    filtro_m = st.selectbox('Mês da Movimentação',meses,index=meses.index(mes_atual))
    filtro_c = st.selectbox('Buscar Cliente',dfeditarentrada["Cliente"].unique())
    editar_status = st.selectbox('Novo Status',["A RECEBER","RECEBIDO"])
    
    dfeditarentrada = df.query('Ano == @filtro_y & Mês == @filtro_m & Cliente == @filtro_c')

with tab3:
    col1, col2 = st.columns([1, 10])

    def obter_indices_selecionados(dfeditar):
        indices_selecionados = []
        
        with col1:
            opcoes = dfeditar.index.tolist()  # Lista de índices do DataFrame
            selected_index = st.selectbox("Selecionar", opcoes)
            if selected_index is not None:
                indices_selecionados.append(selected_index)
        
        return indices_selecionados


    indices_selecionados = obter_indices_selecionados(dfeditarentrada)
    
    dfeditarentrada = dfeditarentrada.query('index ==@indices_selecionados ')
    
    filtro_index = dfeditarentrada
    
    st.table(filtro_index)
   
    

    # if not dfeditarentrada.empty:
    #     filtro_index = dfeditarentrada.index[0]
    #     print(f"O índice do DataFrame é: {filtro_index}")
    # else:
    #     print("O DataFrame está vazio. Nenhum índice pode ser acessado.")

    
    
    # linha3 = filtro_index+2

    # coluna = 6
    
    # with tab3:
    #     with col2:
    #         if st.button("SALVAR EDIÇÃO"):
    #             ws1: Worksheet = sh.get_worksheet(0)
    #             ws1.update_cell(int(linha3), coluna, editar_status)
    #             st.success("Edição salva!")

    # dfeditarentrada["Valor"] = dfeditarentrada["Valor"].apply(lambda x: f'R$ {x:,.2f}')
    # dfeditarentrada = dfeditarentrada.drop(columns=["Ano","Mês","Data"])
    # dfeditarentrada["Data Vencimento"] = pd.to_datetime(dfeditarentrada["Data Vencimento"]).dt.strftime("%d/%m/%Y")
    # with col2:
    #     st.table(dfeditarentrada)
#------------------------------------------------------------------------------------------   
#Entradas em aberto
with tab4:
    st.title("🟢 Recebimentos em Aberto",anchor=False)
    df = df.sort_values(by="Ano",ascending=False)
    entrada_ano = st.selectbox('Escolha um ano',df["Ano"].unique())
    filtro_entrada = st.selectbox("Escolha um mês",meses,index=meses.index(mes_atual))
    aberto = df.query('Mês == @filtro_entrada & Ano == @entrada_ano & Status == "A RECEBER"')
    aberto["Valor"] = aberto["Valor"].apply(lambda x: f'R$ {x:,.2f}')
    aberto = aberto.drop(columns=["Data","Ano","Mês","Tipo"])
    aberto["Data Vencimento"] =pd.to_datetime(aberto["Data Vencimento"]).dt.strftime('%d/%m/%Y')
    st.table(aberto)

#------------------------------------------------------------------------------------------
#Esconder streamlit menus

framegraficos = """
    <style>
    [data-testid="column"]
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
