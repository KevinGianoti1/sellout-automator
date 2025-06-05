import pandas as pd
import os
from datetime import datetime

def gerar_relatorios_por_cliente(df, pasta_destino):
    df.columns = df.columns.str.strip()  # Remove espaços em branco dos nomes de coluna

    if not pd.api.types.is_datetime64_any_dtype(df["Emissão"]):
        df["Emissão"] = pd.to_datetime(df["Emissão"], errors="coerce")

    df["Ano"] = df["Emissão"].dt.year
    df["Mês"] = df["Emissão"].dt.strftime('%b')

    os.makedirs(pasta_destino, exist_ok=True)

    for cliente, grupo in df.groupby("Cliente"):
        grupo_ordenado = grupo.sort_values(by="Emissão")
        ultimo_pedido = grupo_ordenado.iloc[-1]
        representante = ultimo_pedido["Repre"]

        nome_cliente_limpo = cliente.replace("/", "-").replace("\\", "-")
        data_hoje = datetime.today().strftime("%d-%m-%Y")
        pasta_cliente = os.path.join(pasta_destino, nome_cliente_limpo)
        os.makedirs(pasta_cliente, exist_ok=True)

        nome_arquivo = f"Sell Out 2.0 - {nome_cliente_limpo} - {representante} - {data_hoje}.xlsx"
        caminho_arquivo = os.path.join(pasta_cliente, nome_arquivo)

        # Tabela resumo de vendas por mês
        resumo_mensal = grupo_ordenado.pivot_table(
            index="Ano", 
            columns="Mês", 
            values="Total", 
            aggfunc="sum", 
            fill_value=0
        ).reset_index()

        # Tabela de produtos por ano
        produtos_ano = grupo_ordenado.groupby(["Ano", "Descrição"]).agg(
            Qtde=("Qtde", "sum"),
            Total_RS=("Total", "sum"),
            Minimo=("Total", "min"),
            Maximo=("Total", "max")
        ).reset_index()

        with pd.ExcelWriter(caminho_arquivo, engine="xlsxwriter") as writer:
            workbook = writer.book
            formato_titulo = workbook.add_format({
                "bold": True, "font_color": "#FFFFFF", "bg_color": "#305496",
                "border": 1, "align": "center", "valign": "vcenter"
            })
            formato_padrao = workbook.add_format({
                "border": 1, "valign": "vcenter"
            })

            aba = workbook.add_worksheet("Sell Out")
            writer.sheets["Sell Out"] = aba

            # Cabeçalho do cliente
            aba.write("A1", "Cliente:", formato_titulo)
            aba.write("B1", cliente, formato_padrao)
            aba.write("A2", "Representante:", formato_titulo)
            aba.write("B2", representante, formato_padrao)
            aba.write("A3", "Data de Geração:", formato_titulo)
            aba.write("B3", data_hoje, formato_padrao)

            linha = 7  # Espaço reservado

            # Resumo mensal
            aba.write(linha, 0, "Resumo de Vendas por Mês (R$)", formato_titulo)
            resumo_mensal.to_excel(writer, sheet_name="Sell Out", startrow=linha + 1, startcol=0, index=False)
            linha += len(resumo_mensal) + 4

            # Consolidação de produtos
            aba.write(linha, 0, "Consolidação de Produtos por Ano", formato_titulo)
            produtos_ano.to_excel(writer, sheet_name="Sell Out", startrow=linha + 1, startcol=0, index=False)

            # Formatação
            for i, col in enumerate(produtos_ano.columns):
                aba.set_column(i, i, 18)

    print("✅ Relatórios Sell Out 2.0 gerados com sucesso!")
