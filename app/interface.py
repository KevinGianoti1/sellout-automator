import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import os
import tempfile
from datetime import datetime

from sellout.sellout_generator import (
    gerar_sellout,
    plotar_grafico_sellout,
    gerar_resumo_itens,
    salvar_relatorio_completo,
)
from sellout.auth import credentials
from sellout.db import salvar_sellout, buscar_sellout, buscar_resumo


st.set_page_config(page_title="Sell Out Automator", layout="wide")

# LOGIN
authenticator = stauth.Authenticate(
    credentials,
    "sellout_app",       # Nome do cookie
    "authenticator_key", # Chave secreta
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "sidebar")


if authentication_status is False:
    st.error("Usuário ou senha incorretos.")
elif authentication_status is None:
    st.warning("Por favor, faça login para continuar.")
else:
    st.sidebar.success(f"Bem-vindo, {name} 👋")
    authenticator.logout("🔒 Logout", "sidebar")


    # UPLOAD
@@ -56,46 +57,47 @@ else:

        salvar_sellout(name, df_sellout, df_resumo)

        st.success("✅ Dados processados e salvos com sucesso!")

        st.subheader("📅 Tabela de Sell Out")
        st.dataframe(df_sellout.drop(columns=["Data Upload"]), use_container_width=True)

        st.subheader("📉 Gráfico de Vendas")
        st.plotly_chart(plotar_grafico_sellout(df_sellout), use_container_width=True)

        st.subheader("🧾 Resumo de Itens")
        st.dataframe(df_resumo.drop(columns=["Data Upload"]), use_container_width=True)

        st.subheader("📥 Baixar Relatório")
        if st.button("📤 Gerar e Baixar Excel com Sell Out e Resumo"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                salvar_relatorio_completo(df_sellout, df_resumo, tmp.name)
                with open(tmp.name, "rb") as f:
                    st.download_button(
                        "📄 Clique para Baixar",
                        f,
                        file_name=f"sellout_{username}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                os.remove(tmp.name)

    # HISTÓRICO
    st.header("📂 Histórico de Sell Out")
    historico = buscar_sellout(name)
    resumos = buscar_resumo(name)

    if not historico.empty:
        datas = historico["Data Upload"].dropna().unique()
        datas_ordenadas = sorted(datas, reverse=True)
        data_selecionada = st.selectbox("Selecione uma data de upload para visualizar:", datas_ordenadas)

        historico_filtrado = historico[historico["Data Upload"] == data_selecionada]
        resumo_filtrado = resumos[resumos["Data Upload"] == data_selecionada]

        st.subheader("📅 Sell Out da Data Selecionada")
        st.dataframe(historico_filtrado, use_container_width=True)

        st.subheader("🧾 Resumo de Itens da Data Selecionada")
        st.dataframe(resumo_filtrado, use_container_width=True)
    else:
        st.info("Nenhum dado salvo ainda.")
