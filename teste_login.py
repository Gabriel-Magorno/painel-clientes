import streamlit as st
import streamlit_authenticator as stauth

names = ['Gabriel Magorno']
usernames = ['gabriel']
passwords = ['123456']
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(
    {'usernames': {
        usernames[0]: {
            'name': names[0],
            'password': hashed_passwords[0]
        }
    }},
    'login_cookie',
    'abcdef',
    1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'Bem-vindo, {name} 👋')
elif authentication_status is False:
    st.error('Usuário ou senha inválidos')
elif authentication_status is None:
    st.warning('Por favor, insira suas credenciais')
