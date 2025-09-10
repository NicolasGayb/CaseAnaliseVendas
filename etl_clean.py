import sqlite3
import pandas as pd

# --- Conectar ao banco original ---
con = sqlite3.connect("vendas.db")

# --- Extrair dados ---
df_vendas = pd.read_sql_query("SELECT * FROM vendas;", con)
df_clientes = pd.read_sql_query("SELECT * FROM clientes;", con)

# --- Transformar dados ---

# Garantir tipos corretos
df_vendas['valor_venda'] = df_vendas['valor_venda'].astype(float)
df_vendas['custo'] = df_vendas['custo'].astype(float)

# Calcular lucro
df_vendas['lucro'] = df_vendas['valor_venda'] - df_vendas['custo']

# Calcular margem percentual (0 se faturamento = 0)
df_vendas['margem_pct'] = df_vendas.apply(
    lambda x: x['lucro'] / x['valor_venda'] if x['valor_venda'] != 0 else 0,
    axis=1
)

# Adicionar nome e cidade do cliente
df_vendas = df_vendas.merge(df_clientes, on='id_cliente', how='left')

# --- Conferir dados ---
print("Exemplo de vendas transformadas:")
print(df_vendas.head())

# --- Carregar dados transformados no banco ---
df_vendas.to_sql("vendas_limpo", con, if_exists="replace", index=False)

# Fechar conexão
con.close()

# Salvar tabela transformada como CSV
df_vendas.to_csv("vendas_limpo.csv", index=False)
print("CSV 'vendas_limpo.csv' criado com sucesso!")

