import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração inicial do Streamlit
st.set_page_config(page_title="Sistema de Clientes", page_icon="📋", layout="wide")

# Verificação de dependências
try:
    import openpyxl
except ImportError:
    st.error("Por favor, instale o pacote openpyxl usando: pip install openpyxl")
    st.info("Você ainda pode usar o sistema, mas a exportação para Excel não estará disponível.")
    EXCEL_DISPONIVEL = False
else:
    EXCEL_DISPONIVEL = True

# Criação do diretório de exportação se não existir
if not os.path.exists('export'):
    os.makedirs('export')

# Caminho para salvar o arquivo de clientes
FILE_PATH = "clientes.csv"

def carregar_dados_clientes():
    try:
        if os.path.exists(FILE_PATH):
            df = pd.read_csv(FILE_PATH)
            # Converter colunas de data
            date_columns = ['Data de Pagamento', 'Início do Contrato', 'Fim do Contrato']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            return df
        return pd.DataFrame(columns=["Nome", "Mensalidade", "Data de Pagamento", "Início do Contrato", 
                                   "Fim do Contrato", "Duração do Contrato", "Status"])
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame(columns=["Nome", "Mensalidade", "Data de Pagamento", "Início do Contrato", 
                                   "Fim do Contrato", "Duração do Contrato", "Status"])

def salvar_dados_clientes(df):
    try:
        df.to_csv(FILE_PATH, index=False)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")
        return False

# Usuários e senhas
USUARIOS = {
    "gabriel": "123456",
    "maria": "senha123",
    "joao": "senha456"
}

def autenticar(usuario, senha):
    return usuario in USUARIOS and USUARIOS[usuario] == senha

def tela_login():
    st.title("🔐 Sistema de Gerenciamento de Clientes")
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if autenticar(usuario, senha):
                st.session_state.authenticated = True
                st.session_state.usuario = usuario
                st.success(f"Bem-vindo, {usuario}!")
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha inválidos!")

def formatar_data(data):
    try:
        if pd.isna(data):
            return ""
        if isinstance(data, str):
            data = pd.to_datetime(data)
        return data.strftime("%d/%m/%Y")
    except:
        return ""

def painel():
    st.title(f"📋 Gerenciamento de Clientes - Usuário: {st.session_state.usuario}")
    
    # Carregar dados
    clientes = carregar_dados_clientes()
    
    # Tabs para organizar o conteúdo
    tab1, tab2, tab3 = st.tabs(["Cadastro/Edição", "Lista de Clientes", "Exportar/Excluir"])
    
    with tab1:
        with st.form("form_cliente", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_cliente = st.text_input("Nome do Cliente")
                mensalidade = st.number_input("Mensalidade (R$)", min_value=0.0, format="%.2f")
                data_pagamento = st.date_input("Data do Pagamento")
            
            with col2:
                inicio_contrato = st.date_input("Início do Contrato")
                fim_contrato = st.date_input("Fim do Contrato")
                status_pagamento = st.selectbox("Status do Pagamento", ["Pendente", "Pago"])
            
            # Seleção de cliente para edição
            clientes_lista = ["Novo Cliente"] + list(clientes["Nome"].unique()) if not clientes.empty else ["Novo Cliente"]
            cliente_selecionado = st.selectbox("Selecione para editar", clientes_lista)
            
            submitted = st.form_submit_button("Salvar")
            
            if submitted:
                if nome_cliente and mensalidade >= 0:
                    duracao_contrato = (fim_contrato - inicio_contrato).days
                    
                    novo_registro = {
                        "Nome": nome_cliente,
                        "Mensalidade": mensalidade,
                        "Data de Pagamento": data_pagamento,
                        "Início do Contrato": inicio_contrato,
                        "Fim do Contrato": fim_contrato,
                        "Duração do Contrato": duracao_contrato,
                        "Status": status_pagamento
                    }
                    
                    if cliente_selecionado == "Novo Cliente":
                        clientes = pd.concat([clientes, pd.DataFrame([novo_registro])], ignore_index=True)
                        st.success("Cliente cadastrado com sucesso!")
                    else:
                        clientes.loc[clientes["Nome"] == cliente_selecionado] = pd.Series(novo_registro)
                        st.success("Cliente atualizado com sucesso!")
                    
                    salvar_dados_clientes(clientes)
                    st.experimental_rerun()
                else:
                    st.error("Preencha todos os campos obrigatórios!")
    
    with tab2:
        st.write("### Lista de Clientes")
        if not clientes.empty:
            # Formatando as datas para exibição
            clientes_exibicao = clientes.copy()
            for col in ['Data de Pagamento', 'Início do Contrato', 'Fim do Contrato']:
                clientes_exibicao[col] = clientes_exibicao[col].apply(formatar_data)
            
            st.dataframe(clientes_exibicao, use_container_width=True)
        else:
            st.info("Nenhum cliente cadastrado.")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Exportar Dados")
            if EXCEL_DISPONIVEL:
                if st.button("Exportar para Excel"):
                    try:
                        export_path = "export/clientes.xlsx"
                        clientes.to_excel(export_path, index=False)
                        st.success(f"Dados exportados com sucesso para {export_path}")
                    except Exception as e:
                        st.error(f"Erro ao exportar: {str(e)}")
            else:
                st.warning("Exportação para Excel não disponível. Instale o pacote openpyxl.")
        
        with col2:
            st.write("### Excluir Cliente")
            if not clientes.empty:
                cliente_excluir = st.selectbox("Selecione o cliente para excluir", clientes["Nome"].unique())
                if st.button("Excluir", type="primary"):
                    if st.button("Confirmar exclusão"):
                        clientes = clientes[clientes["Nome"] != cliente_excluir]
                        salvar_dados_clientes(clientes)
                        st.success(f"Cliente {cliente_excluir} excluído com sucesso!")
                        st.experimental_rerun()

# Controle de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    tela_login()
else:
    painel()
