-- Criação da tabela clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY,
    nome TEXT,
    cidade TEXT
);

-- Criação da tabela vendas
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

-- Inserindo dados de clientes
INSERT INTO clientes (nome, cidade) VALUES
    ('Ana', 'São Paulo'),
    ('Bruno', 'Curitiba'),
    ('Carla', 'Florianópolis');

-- Inserindo dados de vendas
INSERT INTO vendas (id_cliente, data_venda, valor_venda, custo) VALUES
    (1, '2025-09-01', 1200, 800),
    (2, '2025-09-02', 900, 500),
    (3, '2025-09-03', 1500, 1000),
    (1, '2025-09-04', 700, 400);
