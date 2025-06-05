import streamlit as st
import streamlit_authenticator as stauth

# Gere a senha de forma correta
hashed_password = stauth.Hasher().generate(['123'])[0]

# Config fake para teste
credentials = {
    'usernames': {
        'admin': {
            'email': 'admin@example.com',
            'name': 'Admin',
            'password': hashed_password
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    cookie_name='some_cookie',
    key='some_key',
    cookie_expiry_days=1
)

name, auth_status, username = authenticator.login(location="sidebar", fields={"Form name": "Login"})

if auth_status:
    st.success(f"Bem-vindo, {name}!")
elif auth_status is False:
    st.error("Usuário ou senha inválidos.")
else:
    st.info("Por favor, faça login.")
