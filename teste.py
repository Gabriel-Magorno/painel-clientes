import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados do Excel
df = pd.read_excel('ReceitaMa.xlsx')

# Criar título
st.title('Dashboard de Clientes')

# Exibir resumo dos dados
st.subheader('Resumo dos Dados')
st.write(df.describe())

# Criar gráfico de receita por cliente
st.subheader('Receita por Cliente')
fig, ax = plt.subplots()
df.groupby('Cliente')['Mensalidade'].sum().plot(kind='bar', ax=ax)
st.pyplot(fig)

# Adicionar filtros interativos
cliente_selecionado = st.selectbox('Selecione um cliente:', df['Cliente'].unique())
dados_cliente = df[df['Cliente'] == cliente_selecionado]
st.subheader(f'Dados de {cliente_selecionado}')
st.write(dados_cliente)

