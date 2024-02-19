import streamlit as st
import pandas as pd

def obter_indices_selecionados(df):
    indices_selecionados = []
    for index, row in df.iterrows():
        if st.checkbox('', key=index):
            indices_selecionados.append(index)
    return indices_selecionados

# Dados para o DataFrame
dados = {
    'Item': ['Item 1', 'Item 2', 'Item 3', 'Item 4']
}

# Criar o DataFrame
df = pd.DataFrame(dados)

# Mostrar o DataFrame com checkboxes e obter os índices selecionados
indices_selecionados = obter_indices_selecionados(df)

# Mostrar os índices selecionados
st.write("Índices selecionados:", indices_selecionados)
