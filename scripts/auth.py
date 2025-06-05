import streamlit_authenticator as stauth

# Lista de nomes e usernames dos representantes autorizados
names = [
    "Agnes", "Camila", "Fernanda", "Ana Paula", "Wellington",
    "Bruno", "Vinicius", "Derec", "Matheus"
]

usernames = [
    "agnes", "camila", "fernanda", "ana", "wellington",
    "bruno", "vinicius", "derec", "matheus"
]

# Senhas criptografadas com bcrypt (geradas previamente)
hashed_passwords = [
    "$2b$12$H5fBdZAlJA8riLmp/LUo6eYjbr5.cFYEKOpP1f1gDvYwi8Hp3IHyq",  # 001
    "$2b$12$H8b89xRYsfcj1708Dvj43eQ67Hqv8j/ZOLxsW6v0on4kshpbGg2DO",  # 002
    "$2b$12$iIuRiyQSsdT9I1PVsEome.KzRoVXKrYN9R2zaDSdGIlMvQ766zHCS",  # 003
    "$2b$12$JLIBL0g5PbqxZvgtYbeXKOXXG6XH4nFVOW0ox05EWITmRNIElaIyW",  # 004
    "$2b$12$qEkPc3I.a/LcR9VMCOZpb.T089WigOLxWfp.5fp2MfFwVQGi9nxj6",  # 005
    "$2b$12$bCzd9v8pXqpqTal0ROmDJuOIsnh9tAAWIJqNYGlhvpIaGHPWvwsT.",  # 006
    "$2b$12$Vm3xzqCdz/eYBji4QPmsKO5tS6oKf2LgecJ3hO.QNw47W7Z6D2ge6",  # 007
    "$2b$12$w.MkG0uWJX8NSnLA5z2Pd.ocJVEvXC2KdfJITFgbQA0HT4V4voZsu",  # 008
    "$2b$12$Sujp2szQZgt24CR6VKmSKu1OXIhMww/3zfYityC0fh5XEcRXBhxHW"   # 009
]

# Monta o dicionário de credenciais
credentials = {
    "usernames": {
        username: {
            "name": name,
            "password": hashed
        }
        for username, name, hashed in zip(usernames, names, hashed_passwords)
    }
}

