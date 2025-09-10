import sqlite3
import pandas as pd

conn = sqlite3.connect('vendas.db')
df_clientes = pd.read_sql("SELECT * FROM clientes;", conn)
df_vendas = pd.read_sql("SELECT * FROM vendas;", conn)
df_clientes.to_csv('clientes.csv', index=False)
df_vendas.to_csv('vendas_raw.csv', index=False)
conn.close()
print("CSV exportado: clientes.csv e vendas_raw.csv")