 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index a5f4c679884326bf8d8a8e5725e3d5dffb037e1f..7b1457103839cbd132186b2e5150f6d043cdbb42 100644
--- a/README.md
+++ b/README.md
@@ -13,25 +13,38 @@ O **Sell Out Automator** é uma aplicação desenvolvida com **Streamlit** para
   - 📉 Gráfico de vendas mensal
   - 🧾 Resumo de itens (com totais e preços min/máx)
 - Exportação dos relatórios em Excel
 - Histórico de uploads anteriores
 - Interface limpa, responsiva e amigável
 
 ---
 
 ## 🛠️ Tecnologias Utilizadas
 
 - [Streamlit](https://streamlit.io/)
 - [Pandas](https://pandas.pydata.org/)
 - [Plotly](https://plotly.com/python/)
 - [SQLite](https://www.sqlite.org/index.html)
 - [streamlit-authenticator](https://github.com/mkhorasani/Streamlit-Authenticator)
 
 ---
 
 ## 🚀 Como executar localmente
 
 ### 1. Clone o repositório
 
 ```bash
 git clone https://github.com/KevinGianoti1/sellout-automator.git
 cd sellout-automator
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute a aplicação

```bash
streamlit run app/interface.py
```
