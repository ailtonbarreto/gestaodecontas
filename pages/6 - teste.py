import streamlit as st
import pandas as pd

# Criar um DataFrame de exemplo
data = {'Nome': ['João', 'Maria', 'Pedro'],
        'Idade': [25, 30, 35],
        'Checkbox': [False]}

df = pd.DataFrame(data)

# Exibir o DataFrame com uma coluna de checkboxes
selected_indices = st.multiselect('Selecione linhas:', df.index.tolist())
selected_df = df.iloc[selected_indices]

st.dataframe(selected_df)
