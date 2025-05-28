import pandas as pd
from pathlib import Path

# Caminhos
input_path = Path("data/input")
output_path = Path("data/output")
output_path.mkdir(exist_ok=True)

# Lê o primeiro arquivo Excel encontrado
arquivo = next(input_path.glob("*.xlsx"), None)
if not arquivo:
    raise FileNotFoundError("Nenhum arquivo Excel encontrado na pasta input.")

df = pd.read_excel(arquivo)

# Filtros básicos (ajuste os nomes conforme o seu Excel)
df = df[
    (~df['Categoria'].str.contains('Bonificação|Troca', case=False, na=False)) &
    (~df['Tabela Preço'].str.contains('CUSTO ENTRE EMPRESAS', case=False, na=False)) &
    (~df['Status'].str.contains('Cancelado|Inadimplência', case=False, na=False))
]

# Separar por representante
for rep in df['Representante'].dropna().unique():
    df_rep = df[df['Representante'] == rep]
    caminho = output_path / f"Sell Out 2.0 - {rep}.xlsx"
    df_rep.to_excel(caminho, index=False)
    print(f"✅ Gerado: {caminho.name}")

print("✨ Todos os relatórios foram gerados com sucesso!")

