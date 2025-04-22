import streamlit as st
import pandas as pd
from database import create_table, insert_cliente, get_clientes, delete_cliente, update_cliente
from utils import calcular_duracao

st.set_page_config(page_title="Painel de Clientes", layout="wide")

# Inicializa o banco
create_table()

st.title("📋 Registro de Clientes")

# FORMULÁRIO
with st.form("form_cliente"):
    st.subheader("Cadastrar / Editar Cliente")
    id_editar = st.text_input("ID para editar (deixe em branco para novo cadastro)")
    nome = st.text_input("Nome do Cliente")
    mensalidade = st.number_input("Mensalidade (R$)", step=0.01)
    data_pagamento = st.date_input("Data de Pagamento")
    inicio = st.date_input("Início do Contrato")
    fim = st.date_input("Fim do Contrato")
    status = st.selectbox("Status do Pagamento", ["Pendente", "Feito"])

    submit = st.form_submit_button("Salvar")

    if submit:
        if id_editar:
            update_cliente(id_editar, nome, mensalidade, str(data_pagamento), str(inicio), str(fim), status)
            st.success("Cliente atualizado com sucesso.")
        else:
            insert_cliente(nome, mensalidade, str(data_pagamento), str(inicio), str(fim), status)
            st.success("Cliente cadastrado com sucesso.")

# LISTAGEM
st.subheader("📊 Lista de Clientes")
clientes = get_clientes()

if clientes:
    df = pd.DataFrame(clientes, columns=["ID", "Nome", "Mensalidade", "Pagamento", "Início", "Fim", "Status"])
    df["Duração (dias)"] = df.apply(lambda row: calcular_duracao(row["Início"], row["Fim"]), axis=1)
    st.dataframe(df, use_container_width=True)

    # Exportação
    if st.button("📥 Exportar para Excel"):
        df.to_excel("export/clientes.xlsx", index=False)
        st.success("Arquivo exportado: export/clientes.xlsx")

    # Exclusão
    st.subheader("🗑️ Excluir Cliente")
    id_excluir = st.number_input("ID do cliente a excluir", step=1)
    if st.button("Excluir"):
        delete_cliente(id_excluir)
        st.warning("Cliente excluído.")
else:
    st.info("Nenhum cliente cadastrado ainda.")