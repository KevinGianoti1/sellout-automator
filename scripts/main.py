import pandas as pd
from pathlib import Path

# 📁 Caminhos
input_path = Path("data/input")
output_path = Path("data/output")
output_path.mkdir(exist_ok=True)

# 📥 Localiza o primeiro arquivo .xlsx
arquivo = next(input_path.glob("*.xlsx"), None)
if not arquivo:
    raise FileNotFoundError("Nenhum arquivo Excel encontrado em data/input")

print(f"🔍 Lendo arquivo: {arquivo.name}")
df = pd.read_excel(arquivo)

# 🧮 Calcula o total e extrai o ano da data de emissão
df["Total Calculado"] = df["Qtde"] * df["Valor Unit"]
df["Ano"] = pd.to_datetime(df["Emissão"]).dt.year

# 🧑‍🤝‍🧑 Separar por representante
col_representante = "Repre"
representantes = df[col_representante].dropna().unique()

for rep in representantes:
    df_rep = df[df[col_representante] == rep]
    
    # Organiza colunas na ordem que queremos
    colunas_finais = [
        "Ano", "Emissão", "Notas", "Cliente", "Código", "Descrição",
        "Qtde", "Valor Unit", "Total Calculado", "UF", "Empresa"
    ]
    df_saida = df_rep[colunas_finais].sort_values(by=["Ano", "Emissão"])
    
    # Salva o arquivo
    nome_arquivo = f"Sell Out 2.0 - {rep}.xlsx"
    df_saida.to_excel(output_path / nome_arquivo, index=False)
    print(f"✅ Gerado: {nome_arquivo}")

print("\n🎉 Relatórios por representante gerados com sucesso!")
