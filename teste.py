import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

df = pd.read_excel('ReceitaMa.xlsx')

st.title('Dashboard de Clientes')

st.subheader('Resumo dos dados')
st.write(df.describe())

