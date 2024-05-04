import pyodbc

url_connection = ("DRIVER={SQLite3 ODBC Driver};SERVER=localhost;DATABASE=database")

connection = pyodbc.connect(url_connection)

cursor = connection.cursor()

def add_user(nome, email, status, cursor:pyodbc.Cursor):
    user = get_user_by_email(email, cursor)
    if user == None:
        cursor.execute("""
        INSERT INTO USERS (NAME, EMAIL, STATUS) VALUES (?, ?, ?)
    """, (nome, email, status))
    elif user[2] != status:
        cursor.execute("""
            UPDATE USERS
            SET status = (?)
            WHERE email = (?)
        """, (status, email))

    return get_user_by_email(email, cursor)
    
def get_user_by_email(email, cursor:pyodbc.Cursor):
    cursor.execute(f"SELECT * FROM USERS WHERE EMAIL='{email}'")
    user = cursor.fetchone()
    return user

def get_all_users(cursor:pyodbc.Cursor):
    cursor.execute(f"SELECT * FROM USERS")
    users = cursor.fetchall()
    return users

def add_payment(id_user, status, payment_method, plots, value, cursor:pyodbc.Cursor):
    cursor.execute("""
    INSERT INTO PAYMENTS ( ID_USER, STATUS, PAYMENT_METHOD, PLOTS, VALUE ) VALUES (?, ?, ?, ?, ?)
""", id_user, status, payment_method, plots, value)

    

#user = add_user("Pedro3", "pedro@gmail.com", "Aprovado", cursor)
#print(user)
#get_user_by_email("dev.ceglia.pedro@gmail.com")
#users = get_all_users(cursor)
#print(users)

#cursor.commit()


cursor.close()