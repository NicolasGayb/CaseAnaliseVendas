import sqlite3
import random
from datetime import datetime, timedelta

# -----------------------------
# Funções auxiliares
# -----------------------------

def criar_tabelas(cur):
    """Cria as tabelas clientes e vendas, se não existirem."""
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cidade TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        data_venda DATE NOT NULL,
        valor_venda NUMERIC NOT NULL,
        custo NUMERIC NOT NULL,
        produto TEXT NOT NULL,
        canal_venda TEXT NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
    );
    """)

def popular_clientes(cur):
    """Insere clientes iniciais no banco e retorna lista de IDs."""
    clientes = [
        ("Ana", "São Paulo"),
        ("Bruno", "Curitiba"),
        ("Carla", "Florianópolis"),
        ("Diego", "Rio de Janeiro"),
        ("Elisa", "Belo Horizonte")
    ]
    cur.executemany("INSERT INTO clientes (nome, cidade) VALUES (?, ?);", clientes)
    cur.execute("SELECT id_cliente FROM clientes;")
    return [row[0] for row in cur.fetchall()]

def gerar_vendas(cliente_ids, start_date, end_date):
    """Gera vendas aleatórias coerentes para cada dia do período."""
    vendas = []
    total_days = (end_date - start_date).days + 1

    for day_offset in range(total_days):
        date = start_date + timedelta(days=day_offset)
        num_vendas_hoje = random.randint(0, 5)
        for _ in range(num_vendas_hoje):
            id_cliente = random.choice(cliente_ids)
            valor_venda = random.randint(500, 2000)
            custo = random.randint(200, valor_venda)
            produto = f"Produto {chr(65 + random.randint(0, 4))}"  # Produto A a E
            canal_venda = random.choice(['Online', 'Loja Física'])
            vendas.append((id_cliente, date.strftime("%Y-%m-%d"), valor_venda, custo, produto, canal_venda))
    return vendas

def inserir_vendas(cur, vendas):
    """Insere lista de vendas no banco."""
    cur.executemany("""
    INSERT INTO vendas (id_cliente, data_venda, valor_venda, custo, produto, canal_venda)
    VALUES (?, ?, ?, ?, ?, ?);
    """, vendas)

# -----------------------------
# Execução principal
# -----------------------------

def main():
    # Conectar/criar banco
    with sqlite3.connect("vendas.db") as con:
        cur = con.cursor()

        # Criar tabelas
        criar_tabelas(cur)

        # Popular clientes e pegar IDs
        cliente_ids = popular_clientes(cur)

        # Gerar vendas para todo 2025
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        vendas = gerar_vendas(cliente_ids, start_date, end_date)

        # Inserir vendas no banco
        inserir_vendas(cur, vendas)

    print(f"Banco populado com {len(vendas)} vendas para todo o ano de 2025!")

if __name__ == "__main__":
    main()
