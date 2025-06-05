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

        # --- RESUMO EXECUTIVO ---
        st.header("📊 Resumo Executivo")
        anos = sorted(df_sellout["Ano"].dropna().unique())
        ano_sel = st.selectbox("Ano para análise executiva:", anos, index=len(anos)-1)
        df_ano = df_sellout[df_sellout["Ano"] == ano_sel]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Itens Vendidos", f"{df_resumo[df_resumo['Ano'] == ano_sel]['Qtde_Total'].sum():,.0f}".replace(",", "."))
        col2.metric("Total em Vendas", f"R$ {df_ano.drop(columns=['Cliente', 'Ano']).sum().sum():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col3.metric("Clientes Atendidos", df_ano["Cliente"].nunique())
        col4.metric("Itens Diferentes", df_resumo[df_resumo["Ano"] == ano_sel]["Código"].nunique())

        # --- GRÁFICO ---
        st.subheader("📉 Gráfico de Vendas por Ano")
        anos_grafico = st.multiselect("Filtrar por ano:", anos, default=anos)
        df_grafico = df_sellout[df_sellout["Ano"].isin(anos_grafico)]
        st.plotly_chart(plotar_grafico_sellout(df_grafico), use_container_width=True)

        # --- RESUMO ---
        st.subheader("🧾 Resumo de Itens Vendidos")
        anos_resumo = st.multiselect("Filtrar anos para resumo:", anos, default=anos)
        codigos = df_resumo["Código"].unique()
        clientes = df["Cliente"].unique()
        cod_sel = st.multiselect("Filtrar por código:", codigos, default=codigos)
        cli_sel = st.multiselect("Filtrar por cliente:", clientes, default=clientes)

        df_res_filt = df_resumo[
            (df_resumo["Ano"].isin(anos_resumo)) &
            (df_resumo["Código"].isin(cod_sel)) &
            (df["Cliente"].isin(cli_sel))
        ]

        for ano in sorted(df_res_filt["Ano"].unique()):
            st.markdown(f"### 📆 Ano: {ano}")
            st.dataframe(df_res_filt[df_res_filt["Ano"] == ano].drop(columns=["Data Upload"]), use_container_width=True)

        # --- DOWNLOAD ---
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

    # --- HISTÓRICO ---
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
