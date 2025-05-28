import pandas as pd
from pathlib import Path

# 🛠️ Caminhos
input_path = Path("data/input")
output_path = Path("data/output")
output_path.mkdir(exist_ok=True)

# 📥 Carrega o primeiro arquivo .xlsx da pasta input
arquivo = next(input_path.glob("*.xlsx"), None)
if not arquivo:
    raise FileNotFoundError("Nenhum arquivo .xlsx encontrado na pasta 'data/input'.")

print(f"🔍 Lendo arquivo: {arquivo.name}")
df = pd.read_excel(arquivo)

# 🧼 Filtros iniciais (ajustar nomes das colunas conforme o seu arquivo)
col_categoria = 'Categoria'
col_tabela_preco = 'Tabela Preço'
col_status = 'Status'
col_representante = 'Representante'

df_filtrado = df[
    (~df[col_categoria].str.contains("Bonificação|Troca", case=False, na=False)) &
    (~df[col_tabela_preco].str.contains("CUSTO ENTRE EMPRESAS", case=False, na=False)) &
    (~df[col_status].str.contains("Cancelado|Inadimplência", case=False, na=False))
]

# 👥 Separar por representante e gerar arquivos
representantes = df_filtrado[col_representante].dropna().unique()

for rep in representantes:
    df_rep = df_filtrado[df_filtrado[col_representante] == rep]
    nome_arquivo = f"Sell Out 2.0 - {rep}.xlsx"
    caminho_arquivo = output_path / nome_arquivo
    df_rep.to_excel(caminho_arquivo, index=False)
    print(f"✅ Gerado: {nome_arquivo}")

print("\n🎉 Relatórios gerados com sucesso!")

