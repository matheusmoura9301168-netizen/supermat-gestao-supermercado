# Operações na base de dados (inserir, listar, procurar, atualizar e remover).

import sqlite3

DB = "BDs/Supermat.db"
"""
Anotações
Classes de exceções internas (built-in exceptions), como:
ValueError → usado quando um valor é inválido para uma operação ou função.
TypeError → usado quando o tipo do objeto não é o esperado.
KeyError → usado quando uma chave não existe num dicionário.
IndexError → usado quando o índice não existe numa lista.
"""




def get_conn():
    """
    Abre uma conexão SQLite3 com chaves estrangeiras ativadas.
    Use sempre este helper para garantir integridade referencial.
    """
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    #Cria todas as tabelas se não existirem
    conn = get_conn()
    c = conn.cursor()

def _validate_nonempty(label, value):
    if value is None or str(value).strip() == "":   #verifica se o valor fornecido está nulo (None) ou se é uma ‘string’ vazia (mesmo que contenha apenas espaços).
        raise ValueError(f"{label} é obrigatório.") #raise está a criar e lançando uma exceção do tipo ValueError


def _validate_float(label, value):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} deve ser numérico.")


def _validate_int(label, value):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} deve ser inteiro.")

def adicionar_cliente(ID, nome, senha):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO Clientes (c_ID, c_nome, c_senha) VALUES (?, ?, ?)", (ID, nome, senha))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT c_id, c_nome, c_senha FROM Clientes")
    data = c.fetchall()
    conn.close()
    return data

def remover_cliente(cid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM Clientes WHERE c_id = ?", (cid,))
    conn.commit()
    conn.close()

def procurar_cliente(nome):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT c_id, c_nome, c_senha FROM Clientes WHERE c_nome LIKE ?", (f"%{nome}%",))
    data = c.fetchall()
    conn.close()
    return data


def atualizar_cliente(pid, nome, senha):
    #Atualiza as informações de um cliente no banco de dados.
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        UPDATE Clientes
        SET c_nome = ?, c_senha = ?
        WHERE c_id = ?
    """, (nome, senha, pid))
    conn.commit()
    conn.close()



def adicionar_fornecedor(nome, contato, categoria):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO Fornecedores (F_nome, F_contato, F_categoria) VALUES (?, ?, ?)", (nome, contato, categoria))
    conn.commit()
    conn.close()

def listar_fornecedores():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT F_id, F_nome, F_contato, F_categoria FROM Fornecedores")
    data = c.fetchall()
    conn.close()
    return data

def remover_fornecedor(fid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM Fornecedores WHERE F_id = ?", (fid,))
    conn.commit()
    conn.close()

def procurar_fornecedor(nome):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT F_id, F_nome, F_contato, F_categoria FROM Fornecedores WHERE F_nome LIKE ?", (f"%{nome}%",))
    data = c.fetchall()
    conn.close()
    return data

def atualizar_fornecedor(pid, nome, contato, categoria):

    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        UPDATE Fornecedores
        SET F_nome = ?, F_contato = ?, F_categoria = ?
        WHERE F_id = ?
    """, (nome, contato, categoria, pid))
    conn.commit()
    conn.close()

def adicionar_produto(nome, preco, categoria):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO Produtos (Prod_nome, Prod_preco, Prod_categoria) VALUES (?, ?, ?)", (nome, preco, categoria))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT Prod_id, Prod_nome, Prod_preco, Prod_categoria FROM Produtos")
    data = c.fetchall()
    conn.close()
    return data

def remover_produto(pid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM Produtos WHERE Prod_id = ?", (pid,))
    conn.commit()
    conn.close()

def procurar_produto(nome):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT Prod_id, Prod_nome, Prod_preco, Prod_categoria FROM Produtos WHERE Prod_nome LIKE ?", (f"%{nome}%",))
    data = c.fetchall()
    conn.close()
    return data


def atualizar_produto(pid, nome, preco, categoria):
    #Atualiza as informações de um produto existente no banco de dados.
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        UPDATE Produtos
        SET Prod_nome = ?, Prod_preco = ?, Prod_categoria = ?
        WHERE Prod_id = ?
    """, (nome, preco, categoria, pid))
    conn.commit()
    conn.close()


def adicionar_pedido(cliente_id, produto_id, valor, quantidade):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO Pedidos (P_cliente_id, P_produto_id, P_valor, P_quantidade) VALUES (?, ?, ?, ?)",
              (cliente_id, produto_id, valor, quantidade))
    conn.commit()
    conn.close()

def listar_pedidos():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT p.P_cliente_id, c.c_nome, p.P_produto_id, pr.Prod_nome,
               p.P_valor, p.P_quantidade, p.P_data
        FROM Pedidos p
        JOIN Clientes c ON c.c_id = p.P_cliente_id
        JOIN Produtos pr ON pr.Prod_id = p.P_produto_id
    """)
    data = c.fetchall()
    conn.close()
    return data

def remover_pedido(cliente_id, produto_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM Pedidos WHERE P_cliente_id = ? AND P_produto_id = ?", (cliente_id, produto_id))
    conn.commit()
    conn.close()

def adicionar_encomenda(fornecedor_id, produto_id, valor):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO Encomendas (E_fornecedor_id, E_produtos_id, E_valor) VALUES (?, ?, ?)",
              (fornecedor_id, produto_id, valor))
    conn.commit()
    conn.close()

def listar_encomendas():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT e.E_id, f.F_nome, p.Prod_nome, e.E_valor, e.E_data,
               e.E_fornecedor_id, e.E_produtos_id
        FROM Encomendas e
        JOIN Fornecedores f ON f.F_id = e.E_fornecedor_id
        JOIN Produtos p ON p.Prod_id = e.E_produtos_id
    """)
    data = c.fetchall()
    conn.close()
    return data

def remover_encomenda(eid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM Encomendas WHERE E_id = ?", (eid,))
    conn.commit()
    conn.close()
