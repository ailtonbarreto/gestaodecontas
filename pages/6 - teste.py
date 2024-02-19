import streamlit as st
import pandas as pd
from qgrid import qgrid

# Criar um DataFrame de exemplo
data = {'Nome': ['João', 'Maria', 'Pedro'],
        'Idade': [25, 30, 35],
        'Checkbox': [False, True, False]}

df = pd.DataFrame(data)

# Criar um widget QGrid com o DataFrame
qgrid_widget = qgrid.show_grid(df, show_toolbar=False)

# Exibir o widget QGrid no Streamlit
st.write(qgrid_widget)
# asdf
