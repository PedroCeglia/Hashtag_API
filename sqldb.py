import sqlite3

# Nome do arquivo do banco de dados SQLite
database_file = "database"

def initialize_database():
    # Conecta ao banco de dados ou cria um novo se não existir
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Cria tabela de usuários se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        ID INTEGER PRIMARY KEY,
        NAME TEXT NOT NULL,
        EMAIL TEXT NOT NULL UNIQUE,
        STATUS TEXT NOT NULL
    )
    """)

    # Cria tabela de pagamentos se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PAYMENTS (
        ID INTEGER PRIMARY KEY,
        ID_USER INTEGER,
        STATUS TEXT NOT NULL,
        PAYMENT_METHOD TEXT NOT NULL,
        PLOTS INTEGER NOT NULL,
        VALUE REAL NOT NULL,
        FOREIGN KEY (ID_USER) REFERENCES USERS(ID)
    )
    """)

    connection.commit()
    connection.close()

def add_user(nome, email, status):
    # Conecta ao banco de dados
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Verifica se o usuário já existe
    cursor.execute("SELECT * FROM USERS WHERE EMAIL=?", (email,))
    existing_user = cursor.fetchone()

    if existing_user is None:
        # Insere novo usuário
        cursor.execute("""
        INSERT INTO USERS (NAME, EMAIL, STATUS) VALUES (?, ?, ?)
        """, (nome, email, status))
    elif existing_user[3] != status:  # Verifica se o status do usuário mudou
        cursor.execute("""
            UPDATE USERS
            SET STATUS = ?
            WHERE EMAIL = ?
        """, (status, email))

    connection.commit()
    connection.close()

def get_user_by_email(email):
    # Conecta ao banco de dados
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Procura usuário pelo email
    cursor.execute("SELECT * FROM USERS WHERE EMAIL=?", (email,))
    user = cursor.fetchone()

    connection.close()
    return user

def get_all_users():
    # Conecta ao banco de dados
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Retorna todos os usuários
    cursor.execute("SELECT * FROM USERS")
    users = cursor.fetchall()

    connection.close()
    return users

def add_payment(id_user, status, payment_method, plots, value):
    # Conecta ao banco de dados
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Insere novo pagamento
    cursor.execute("""
    INSERT INTO PAYMENTS (ID_USER, STATUS, PAYMENT_METHOD, PLOTS, VALUE)
    VALUES (?, ?, ?, ?, ?)
    """, (id_user, status, payment_method, plots, value))

    connection.commit()
    connection.close()

# Inicializa o banco de dados
initialize_database()

# Exemplo de uso
add_user("Pedro3", "pedro7777@gmail.com", "Aprovado")
# user = get_user_by_email("pedro@gmail.com")
# print(user)
# users = get_all_users()
# print(users)
# add_payment(1, "Aprovado", "Cartão de Crédito", 1, 100.00)
