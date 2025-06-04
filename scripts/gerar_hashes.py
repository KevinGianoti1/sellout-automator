import streamlit_authenticator as stauth

# Senhas simples (somente para teste)
senhas = ['001', '002', '003', '004', '005', '006', '007', '008', '009']

# Gera os hashes
hashes = stauth.Hasher(senhas).generate()

# Exibe cada hash gerado
for h in hashes:
    print(h)
