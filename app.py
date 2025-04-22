import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Caminho para salvar o arquivo de clientes (CSV ou Excel)
FILE_PATH = "clientes.csv"  # Pode ser alterado para "clientes.xlsx" se preferir Excel

# Função para carregar os dados dos clientes do arquivo (CSV ou Excel)
def carregar_dados_clientes():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)  # Carrega o arquivo CSV
    else:
        return pd.DataFrame(columns=["Nome", "Mensalidade", "Data de Pagamento", "Início do Contrato", "Fim do Contrato", "Duração do Contrato", "Status"])

# Função para salvar os dados dos clientes no arquivo (CSV ou Excel)
def salvar_dados_clientes(df):
    df.to_csv(FILE_PATH, index=False)  # Salva o DataFrame no arquivo CSV

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

# Função de login
def tela_login():
    st.title("🔐 Login")
    usuario = st.text_input("Usuário", "")
    senha = st.text_input("Senha", "", type="password")
    
    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state.authenticated = True  # Define o estado de autenticação
            st.session_state.usuario = usuario  # Armazena o nome de usuário
            st.session_state.first_login = False  # Marca que o login foi realizado
            st.success(f"Bem-vindo, {usuario}!")
            st.experimental_rerun()  # Recarrega a página para mostrar o painel
        else:
            st.error("Usuário ou senha inválidos!")

# Função de exibição do painel de clientes
def painel():
    st.title("📋 Registro de Clientes")
    
    # Carregar os dados de clientes do arquivo
    clientes = carregar_dados_clientes()
    
    # Formatação das datas para o formato brasileiro (DD/MM/YYYY)
    def formatar_data(data):
        return data.strftime("%d/%m/%Y") if isinstance(data, datetime) else data

    # Formulário para adicionar ou editar um cliente
    with st.form("form_cliente"):
        nome_cliente = st.text_input("Nome do Cliente", key="nome_cliente")
        mensalidade = st.number_input("Mensalidade", min_value=0.0, format="%.2f", key="mensalidade")
        data_pagamento = st.date_input("Data do Pagamento", key="data_pagamento", format="DD/MM/YYYY")
        inicio_contrato = st.date_input("Início do Contrato", key="inicio_contrato", format="DD/MM/YYYY")
        fim_contrato = st.date_input("Fim do Contrato", key="fim_contrato", format="DD/MM/YYYY")
        status_pagamento = st.selectbox("Status do Pagamento", ["Pago", "Pendente"], key="status_pagamento")
        
        # Editar cliente
        cliente_para_editar = st.selectbox("Selecione um cliente para editar", ["Selecione um cliente"] + list(clientes["Nome"].unique()))
        submitted = st.form_submit_button("Adicionar ou Editar Cliente")
        
        if submitted:
            if nome_cliente and mensalidade and data_pagamento and inicio_contrato and fim_contrato:
                # Calculando a duração do contrato
                duracao_contrato = (fim_contrato - inicio_contrato).days
                
                if cliente_para_editar == "Selecione um cliente":
                    # Caso seja um novo cliente, adicionar na tabela
                    novo_cliente = pd.DataFrame([[nome_cliente, mensalidade, data_pagamento, inicio_contrato, fim_contrato, duracao_contrato, status_pagamento]], columns=clientes.columns)
                    clientes = pd.concat([clientes, novo_cliente], ignore_index=True)
                    st.success(f"Cliente {nome_cliente} adicionado com sucesso!")
                else:
                    # Caso seja um cliente existente, editar os dados
                    clientes.loc[clientes["Nome"] == cliente_para_editar, ["Nome", "Mensalidade", "Data de Pagamento", "Início do Contrato", "Fim do Contrato", "Duração do Contrato", "Status"]] = [
                        nome_cliente, mensalidade, data_pagamento, inicio_contrato, fim_contrato, duracao_contrato, status_pagamento
                    ]
                    st.success(f"Cliente {nome_cliente} editado com sucesso!")

                salvar_dados_clientes(clientes)  # Salvar os dados atualizados no arquivo
                
                # Limpar os campos de input após o cadastro ou edição
                st.session_state.nome_cliente = ""  # Limpar o campo Nome
                st.session_state.mensalidade = 0.0  # Limpar o campo Mensalidade
                st.session_state.data_pagamento = ""  # Limpar o campo Data de Pagamento
                st.session_state.inicio_contrato = ""  # Limpar o campo Início do Contrato
                st.session_state.fim_contrato = ""  # Limpar o campo Fim do Contrato
                st.session_state.status_pagamento = ""  # Limpar o campo Status de Pagamento
                st.experimental_rerun()  # Recarrega a página para limpar os campos

            else:
                st.error("Por favor, preencha todos os campos!")

    # Exibindo a tabela de clientes
    st.write("### Lista de Clientes")
    # Formatar as datas para o padrão brasileiro (DD/MM/YYYY)
    clientes["Data de Pagamento"] = clientes["Data de Pagamento"].apply(lambda x: formatar_data(x))
    clientes["Início do Contrato"] = clientes["Início do Contrato"].apply(lambda x: formatar_data(x))
    clientes["Fim do Contrato"] = clientes["Fim do Contrato"].apply(lambda x: formatar_data(x))
    st.dataframe(clientes)

    # Opção de exportar os dados para Excel
    if st.button("Exportar para Excel"):
        clientes.to_excel("export/clientes.xlsx", index=False)
        st.success(f"Arquivo exportado para: export/clientes.xlsx")

    # Opção de excluir clientes
    cliente_para_excluir = st.selectbox("Selecione um cliente para excluir", clientes["Nome"])
    if st.button("Excluir Cliente"):
        clientes = clientes[clientes["Nome"] != cliente_para_excluir]
        salvar_dados_clientes(clientes)  # Salvar após exclusão
        st.success(f"Cliente {cliente_para_excluir} excluído com sucesso!")

# Verificando se o usuário está autenticado
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    tela_login()  # Se não estiver autenticado, mostra a tela de login
else:
    painel()  # Se estiver autenticado, mostra o painel

