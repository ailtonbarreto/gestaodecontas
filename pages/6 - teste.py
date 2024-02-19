import streamlit as st
import pandas as pd

# Criar um DataFrame de exemplo
data = {'Nome': ['João', 'Maria', 'Pedro'],
        'Idade': [25, 30, 35],
        'Checkbox': [False, True, False]}

df = pd.DataFrame(data)

# Exibir o DataFrame com uma coluna de checkboxes editável
for i, row in df.iterrows():
    checkbox_state = st.checkbox(label='', value=row['Checkbox'], key=i)
    df.at[i, 'Checkbox'] = checkbox_state

st.dataframe(df)
