import sqlite3
import random
from datetime import datetime, timedelta

# Conectar/criar banco
con = sqlite3.connect("vendas.db")
cur = con.cursor()

# --- Criar tabelas ---

# Clientes
cur.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cidade TEXT
);
""")

# Vendas
cur.execute("""
CREATE TABLE IF NOT EXISTS vendas (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    data_venda DATE,
    valor_venda NUMERIC,
    custo NUMERIC,
    produto TEXT,
    canal_venda TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
""")

# --- Popular clientes ---
clientes = [
    ("Ana", "São Paulo"),
    ("Bruno", "Curitiba"),
    ("Carla", "Florianópolis"),
    ("Diego", "Rio de Janeiro"),
    ("Elisa", "Belo Horizonte")
]

cur.executemany("INSERT INTO clientes (nome, cidade) VALUES (?, ?);", clientes)

# --- Popular vendas coerentes para todo 2025 ---
vendas = []
cliente_ids = [1, 2, 3, 4, 5]  # IDs de clientes já criados
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
total_days = (end_date - start_date).days + 1

# Vamos gerar vendas aleatórias diariamente
for day_offset in range(total_days):
    date = start_date + timedelta(days=day_offset)
    num_vendas_hoje = random.randint(0, 5)  # 0 a 5 vendas por dia
    for _ in range(num_vendas_hoje):
        id_cliente = random.choice(cliente_ids)
        valor_venda = random.randint(500, 2000)
        custo = random.randint(200, valor_venda)  # custo ≤ valor_venda
        produto = f"Produto {chr(65 + random.randint(0,4))}"  # Produto A a E
        canal_venda = random.choice(['Online', 'Loja Física'])
        vendas.append((id_cliente, date.strftime("%Y-%m-%d"), valor_venda, custo, produto, canal_venda))

# Inserir vendas no banco
cur.executemany("""
INSERT INTO vendas (id_cliente, data_venda, valor_venda, custo, produto, canal_venda)
VALUES (?, ?, ?, ?, ?, ?);
""", vendas)

# --- Finalizar ---
con.commit()
con.close()
print(f"Banco populado com {len(vendas)} vendas para todo o ano de 2025!")
