import streamlit as st
import pandas as pd
import os
import tempfile
from datetime import datetime

import sys
from pathlib import Path

# Adiciona o diretório raiz (acima de 'app/') ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.sellout_generator import (
    gerar_sellout,
    plotar_grafico_sellout,
    gerar_resumo_itens,
    salvar_relatorio_completo,
)
from scripts.db import salvar_sellout, buscar_sellout, buscar_resumo

st.set_page_config(page_title="Sell Out Automator", layout="wide")

# ----- LOGIN SIMPLES -----
USUARIOS = {
    "agnes": "001",
    "camila": "002",
    "fernanda": "003",
    "ana": "004",
    "wellington": "005",
    "bruno": "006",
    "vinicius": "007",
    "derec": "008",
    "matheus": "009",
}

if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = ""

if not st.session_state.logado:
    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario in USUARIOS and senha == USUARIOS[usuario]:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.success(f"Bem-vindo, {usuario} 👋")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
else:
    st.sidebar.success(f"Logado como: {st.session_state.usuario} ✅")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.session_state.usuario = ""
        st.rerun()

    # UPLOAD
    arquivo = st.file_uploader("📁 Envie seu arquivo de vendas (.xlsx)", type=["xlsx"])

    if arquivo:
        df = pd.read_excel(arquivo)
        df.columns = df.columns.str.strip()
        df["Emissão"] = pd.to_datetime(df["Emissão"], errors="coerce")
        df["Ano"] = df["Emissão"].dt.year
        df["Mês"] = df["Emissão"].dt.month
        df["Representante"] = st.session_state.usuario

        df_sellout = gerar_sellout(df)
        df_resumo = gerar_resumo_itens(df)

        data_upload = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_sellout["Data Upload"] = data_upload
        df_resumo["Data Upload"] = data_upload

        salvar_sellout(st.session_state.usuario, df_sellout, df_resumo)

        st.success("✅ Dados processados e salvos com sucesso!")

        st.subheader("📅 Tabela de Sell Out")
        st.dataframe(df_sellout.drop(columns=["Data Upload"]), use_container_width=True)

        st.subheader("📉 Gráfico de Vendas")
        anos_disponiveis = sorted(df_sellout["Ano"].dropna().unique())
        anos_selecionados = st.multiselect("Selecione o(s) ano(s) para o gráfico:", anos_disponiveis, default=anos_disponiveis)
        df_filtrado = df_sellout[df_sellout["Ano"].isin(anos_selecionados)]
        st.plotly_chart(plotar_grafico_sellout(df_filtrado), use_container_width=True)

        st.subheader("🧾 Resumo de Itens por Ano")
        for ano in sorted(df_resumo["Ano"].unique()):
            st.markdown(f"### 📆 Ano: {ano}")
            st.dataframe(df_resumo[df_resumo["Ano"] == ano].drop(columns=["Data Upload"]), use_container_width=True)

        st.subheader("📅 Baixar Relatório")
        if st.button("📄 Gerar e Baixar Excel com Sell Out e Resumo"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                salvar_relatorio_completo(df_sellout, df_resumo, tmp.name)
                with open(tmp.name, "rb") as f:
                    st.download_button(
                        "📄 Clique para Baixar",
                        f,
                        file_name=f"sellout_{st.session_state.usuario}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                os.remove(tmp.name)

    # HISTÓRICO
    st.header("📂 Histórico de Sell Out")
    historico = buscar_sellout(st.session_state.usuario)
    resumos = buscar_resumo(st.session_state.usuario)

    if not historico.empty:
        datas = historico["Data Upload"].dropna().unique()
        datas_ordenadas = sorted(datas, reverse=True)
        data_selecionada = st.selectbox("Selecione uma data de upload para visualizar:", datas_ordenadas)

        historico_filtrado = historico[historico["Data Upload"] == data_selecionada]
        resumo_filtrado = resumos[resumos["Data Upload"] == data_selecionada]

        st.subheader("📅 Sell Out da Data Selecionada")
        st.dataframe(historico_filtrado, use_container_width=True)

        st.subheader("🧾 Resumo de Itens da Data Selecionada por Ano")
        for ano in sorted(resumo_filtrado["Ano"].unique()):
            st.markdown(f"### 📆 Ano: {ano}")
            st.dataframe(resumo_filtrado[resumo_filtrado["Ano"] == ano], use_container_width=True)
    else:
        st.info("Nenhum dado salvo ainda.")
