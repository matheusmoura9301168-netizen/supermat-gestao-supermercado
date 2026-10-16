# Cria a base de dados BDs/Supermat.db.

import sqlite3   # Biblioteca para trabalhar com SQLite
from pathlib import Path  # Usada para garantir que o diretório do banco exista

# Caminho do banco de dados
DB = "BDs/Supermat.db"

# Criar diretório automaticamente se não existir
Path(DB).parent.mkdir(parents=True, exist_ok=True)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect(DB)
cursor = conn.cursor()
# Ativar integridade referencial (chaves estrangeiras funcionarem corretamente)
cursor.execute("PRAGMA foreign_keys = ON;")

# Criação das tabelas

cursor.execute("""
CREATE TABLE IF NOT EXISTS Clientes (
    c_id INTEGER PRIMARY KEY,
    c_nome TEXT NOT NULL UNIQUE,
    c_senha TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Fornecedores (
    F_id INTEGER PRIMARY KEY AUTOINCREMENT,
    F_nome TEXT NOT NULL,
    F_contato TEXT,
    F_categoria TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Produtos (
    Prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Prod_nome TEXT NOT NULL,
    Prod_preco REAL NOT NULL,
    Prod_categoria TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Pedidos (
    P_cliente_id INTEGER NOT NULL,
    P_produto_id INTEGER NOT NULL,
    P_valor REAL NOT NULL,
    P_quantidade INTEGER NOT NULL CHECK (P_quantidade > 0),
    P_data TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (P_cliente_id) REFERENCES Clientes(c_id) ON DELETE CASCADE,
    FOREIGN KEY (P_produto_id) REFERENCES Produtos(Prod_id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Encomendas (
    E_id INTEGER PRIMARY KEY AUTOINCREMENT,
    E_fornecedor_id INTEGER NOT NULL,
    E_produtos_id INTEGER NOT NULL,
    E_data TEXT DEFAULT (datetime('now')),
    E_valor REAL NOT NULL,
    FOREIGN KEY (E_produtos_id) REFERENCES Produtos(Prod_id) ON DELETE CASCADE,
    FOREIGN KEY (E_fornecedor_id) REFERENCES Fornecedores(F_id) ON DELETE CASCADE
);
""")

conn.commit()
conn.close()
print("Sucesso!")
