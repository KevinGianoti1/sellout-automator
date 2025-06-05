import sqlite3
import pandas as pd
from datetime import datetime

# 🔌 Conecta ao banco SQLite
def conectar():
    return sqlite3.connect("data/historico.db")

# 💾 Salva Sell Out e Resumo no banco
def salvar_sellout(usuario, df_sellout, df_resumo):
    conn = conectar()
    data_upload = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Cópia para evitar mutações no dataframe original
    df_sellout = df_sellout.copy()
    df_resumo = df_resumo.copy()

    df_sellout["Usuario"] = usuario
    df_resumo["Usuario"] = usuario
    df_sellout["Data Upload"] = data_upload
    df_resumo["Data Upload"] = data_upload

    df_sellout.to_sql("sellout", conn, if_exists="append", index=False)
    df_resumo.to_sql("resumo", conn, if_exists="append", index=False)

    conn.close()

# 💾 Salva apenas o Resumo
def salvar_resumo(usuario, df):
    conn = conectar()
    df = df.copy()
    df["Usuario"] = usuario
    df["Data Upload"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_sql("resumo", conn, if_exists="append", index=False)
    conn.close()

# 🔍 Busca histórico de Sell Out do usuário
def buscar_sellout(usuario):
    conn = conectar()
    try:
        df = pd.read_sql(
            "SELECT * FROM sellout WHERE Usuario = ?",
            conn,
            params=(usuario,)
        )
    except Exception:
        df = pd.DataFrame()  # Retorna vazio se erro
    conn.close()
    return df

# 🔍 Busca histórico de Resumo do usuário
def buscar_resumo(usuario):
    conn = conectar()

    # 🔐 Cria a tabela 'resumo' caso ainda não exista
    conn.execute("""
        CREATE TABLE IF NOT EXISTS resumo (
            Ano INTEGER,
            Código TEXT,
            Descrição TEXT,
            Qtde_Total INTEGER,
            Valor_Total TEXT,
            Preço_Mínimo TEXT,
            Preço_Máximo TEXT,
            Usuario TEXT,
            "Data Upload" TEXT
        )
    """)

    try:
        df = pd.read_sql(
            "SELECT * FROM resumo WHERE Usuario = ?",
            conn,
            params=(usuario,)
        )
    except Exception:
        df = pd.DataFrame()
    
    conn.close()
    return df
