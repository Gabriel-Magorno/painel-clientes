import streamlit as st
import pandas as pd
import os

# Usuários e senhas armazenados no código (você pode adicionar mais)
USUARIOS = {
    "gabriel": "123456",  # Nome de usuário e senha
    "maria": "senha123",
    "joao": "senha456"
}

def autenticar(usuario, senha):
    if usuario in USUARIOS and USUARIOS[usuario] == senha:
        return True
    return False

# Função para criar a pasta 'export' se não existir
def criar_pasta_export():
    if not os.path.exists("export"):
        os.makedirs("export")

# Função de login
def tela_login():
    st.title("🔐 Login")
    usuario = st.text_input("Usuário", "")
    senha = st.text_input("Senha", "", type="password")
    
    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state.authenticated = True  # Define o estado de autenticação
            st.session_state.usuario = usuario  # Armazena o nome de usuário
            st.success(f"Bem-vindo, {usuario}!")
        else:
            st.error("Usuário ou senha inválidos!")

# Função de exibição do painel de clientes
def painel():
    st.title("📋 Registro de Clientes")
    
    # Verificando se já existe a tabela no session_state, senão cria uma tabela vazia
    if 'clientes' not in st.session_state:
        st.session_state.clientes = pd.DataFrame(columns=["Nome", "Mensalidade", "Data de Pagamento", "Início do Contrato", "Fim do Contrato", "Duração do Contrato", "Status"])
    
    clientes = st.session_state.clientes
    
    # Formulário para adicionar novo cliente
    with st.form("form_cliente"):
        nome_cliente = st.text_input("Nome do Cliente")
        mensalidade = st.number_input("Mensalidade", min_value=0.0, format="%.2f")
        data_pagamento = st.date_input("Data do Pagamento")
        inicio_contrato = st.date_input("Início do Contrato")
        fim_contrato = st.date_input("Fim do Contrato")
        status_pagamento = st.selectbox("Status do Pagamento", ["Pago", "Pendente"])
        submitted = st.form_submit_button("Adicionar Cliente")

        if submitted:
            if nome_cliente and mensalidade and data_pagamento and inicio_contrato and fim_contrato:
                # Calculando a duração do contrato
                duracao_contrato = (fim_contrato - inicio_contrato).days
                novo_cliente = pd.DataFrame([[nome_cliente, mensalidade, data_pagamento, inicio_contrato, fim_contrato, duracao_contrato, status_pagamento]], columns=clientes.columns)
                
                # Adicionando o novo cliente na tabela existente
                st.session_state.clientes = pd.concat([clientes, novo_cliente], ignore_index=True)
                st.success(f"Cliente {nome_cliente} adicionado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos!")

    # Exibindo a tabela de clientes
    st.write("### Lista de Clientes")
    st.dataframe(clientes)

    # Opção de exportar os dados para Excel
    if st.button("Exportar para Excel"):
        criar_pasta_export()
        file_path = "export/clientes.xlsx"
        clientes.to_excel(file_path, index=False)
        st.success(f"Arquivo exportado para: {file_path}")

    # Opção de excluir clientes
    cliente_para_excluir = st.selectbox("Selecione um cliente para excluir", clientes["Nome"])
    if st.button("Excluir Cliente"):
        st.session_state.clientes = clientes[clientes["Nome"] != cliente_para_excluir]
        st.success(f"Cliente {cliente_para_excluir} excluído com sucesso!")

# Verificando se o usuário está autenticado
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    tela_login()  # Se não estiver autenticado, mostra a tela de login
else:
    painel()  # Se estiver autenticado, mostra o painel
