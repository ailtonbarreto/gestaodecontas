#Adiciona Saída

import streamlit as st
import pandas as pd
import gspread as sg
from gspread import Worksheet

#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",page_title="Adicionar Saída",initial_sidebar_state='collapsed',page_icon='📊')
st.sidebar.link_button("Ver Planilha","https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

tab1, tab2, tab3, tab4 = st.tabs(["Adicionar Saída","Excluir Saída","Editar Status de Saída","Pagamentos em Aberto"])


# ----------------------------------------------------------------------------------------
# Dados Saídas

gc = sg.service_account("gestao.json")
url = 'https://docs.google.com/spreadsheets/d/1HcISrCFCKWOtF6O_RonxH_RVdg2jFBly2KQryc_cZcY/edit?usp=sharing'
sh = gc.open_by_url(url)
ws = sh.get_worksheet(1)
planilha = ws.get_all_values()
df = pd.DataFrame(planilha[1:], columns=planilha[0])

df['Data'] = pd.to_datetime(df["Data Emissão"])
df["Ano"] = df["Data"].dt.year
df["Mês"] = df["Data"].dt.month
df.sort_values("Data", inplace=True)
df["Ano"] = df["Ano"].astype(int)
df["Mês"] = df["Mês"].astype(int)
df['Valor'] = df['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)


#----------------------------------------------------------------------------------------
#cadastro de fornecedores
dfcadastro = sh.get_worksheet(2)
dfcadastro = dfcadastro.get_all_values()
planilhacadastro = pd.DataFrame(dfcadastro[1:], columns=dfcadastro[0])


#----------------------------------------------------------------------------------------
#Função definir meses


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
#dicionário classificar meses

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
df = df.sort_values(by='Ordem_Mês',ascending = True).drop(columns=['Ordem_Mês'])
df = df.sort_values("Ano",ascending=False)
#----------------------------------------------------------------------------------------
# Adicionar Saída

with tab1:
    st.title("🔴 Adicionar Saída",anchor=False)

    entrada_data = st.date_input("Data","today",format= "DD/MM/YYYY")

    entrada_fornecedor = st.selectbox("Fornecedor",planilhacadastro["Fornecedor"])
    
    entrada_categoria = planilhacadastro.query(f'Fornecedor == "{entrada_fornecedor}"')['Categoria'].iloc[0]

    entrada_valor = st.text_input("Valor",value="0,00")

    entrada_status = st.selectbox("Status",["PAGO","A PAGAR"])


    if st.button("ADICIONAR SAÍDA"):
    # Carregar planilha do google sheets
        ws: Worksheet = sh.get_worksheet(1)

    # Criar uma nova linha com os dados inseridos
        entrada_data = entrada_data.strftime("%Y-%m-%d")
        nova_linha = [entrada_data, entrada_fornecedor, entrada_categoria, entrada_valor, entrada_status,"SAÍDA"]
    
    # Adicionar a nova linha à planilha
        ws.append_row(nova_linha)
   
        st.success("Movimentação salva!")
    
# #------------------------------------------------------------------------------------------
#Remover linha
    
with tab2:

    st.title("🔴 Excluir Saída",anchor=False)
#Indice da linha a ser removida
    dfdelete = df
    filtro_ano = st.selectbox("Ano",dfdelete["Ano"].unique())
    filtro_mes = st.selectbox("Mês",dfdelete["Mês"].unique())
    filtro_fornecedor = st.selectbox('Fornecedor',dfdelete["Fornecedor"].unique())
    linha1 = st.number_input("Excluir Linha",format="%.0f")

    dfdelete = dfdelete.query('Ano == @filtro_ano & Mês == @filtro_mes & Fornecedor == @filtro_fornecedor')

    if st.button("EXCLUIR SAÍDA"):
        
        wsremover: Worksheet = sh.get_worksheet(1)
    
        wsremover.delete_rows(int(linha1) + 2)
    
        st.success("Saída Excluída Com Sucesso!")

    st.table(dfdelete)
    
#------------------------------------------------------------------------------------------ 
# Editar uma saída  

with tab3:
     st.title("🔴 Editar Status",anchor=False)

     dfeditar = df
    
     #Dados da linha editada
     filtro_y = st.selectbox('Ano da Movimentação',dfeditar["Ano"].unique())
     filtro_m = st.selectbox('Mês da Movimentação',dfeditar["Mês"].unique())
     filtro_f = st.selectbox('Buscar Fornecedor',dfeditar["Fornecedor"].unique())
     
     editar_status = st.selectbox('Novo Status',["A PAGAR","PAGO"])
    


     dfeditar = df.query('Ano == @filtro_y & Mês == @filtro_m & Fornecedor == @filtro_f')

with tab3:
    col1, col2 = st.columns([1,10])
    def obter_indices_selecionados(dfeditar):
        indices_selecionados = []
        
        with col1:
            for index, row in dfeditar.iterrows():
                if st.checkbox(f'Selecionar linha {index}', True, key=index):
                    indices_selecionados.append(index)
            return indices_selecionados
    
       
    indices_selecionados = obter_indices_selecionados(dfeditar)

    dfeditar = dfeditar.query('index ==@indices_selecionados ')

    filtro_index = dfeditar.index[0]

    linha3 = filtro_index+2

    coluna = 5
    
    with tab3:
        if st.button("SALVAR EDIÇÃO"):
            ws1: Worksheet = sh.get_worksheet(1)
            ws1.update_cell(int(linha3), coluna, editar_status)
            st.success("Edição salva!")

    df["Valor"] = df["Valor"].apply(lambda x: f'R$ {x:.2f}')
    with col2:
        st.table(dfeditar)
#------------------------------------------------------------------------------------------
#Saídas em aberto
 
with tab4:
    st.title("🔴 Pagamentos em Aberto",anchor=False)
    entrada_ano = st.selectbox('Escolha um ano',df["Ano"].unique())
    filtro_entrada = st.selectbox("Escolha um mês",df["Mês"].unique())
    aberto = df.query('Mês == @filtro_entrada & Ano == @entrada_ano & Status == "A PAGAR"')
    aberto = aberto.drop(columns=["Data","Ano","Mês","Tipo"])
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