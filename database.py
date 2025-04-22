import sqlite3

def connect_db():
    return sqlite3.connect('clientes.db')

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            mensalidade REAL,
            data_pagamento TEXT,
            inicio_contrato TEXT,
            fim_contrato TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_cliente(nome, mensalidade, data_pagamento, inicio, fim, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, mensalidade, data_pagamento, inicio_contrato, fim_contrato, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, mensalidade, data_pagamento, inicio, fim, status))
    conn.commit()
    conn.close()

def get_clientes():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_cliente(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_cliente(id, nome, mensalidade, data_pagamento, inicio, fim, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nome = ?, mensalidade = ?, data_pagamento = ?, inicio_contrato = ?, fim_contrato = ?, status = ?
        WHERE id = ?
    """, (nome, mensalidade, data_pagamento, inicio, fim, status, id))
    conn.commit()
    conn.close()
