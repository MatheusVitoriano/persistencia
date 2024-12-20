import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor


def get_connection():
        return psycopg2.connect(host="localhost", database="db1", user="postgres", password="123456", port="5432")

def create_usuario(nome: str, email: str):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # SQL correto
        cursor.execute(
            "INSERT INTO usuario (nome, email) VALUES (%s, %s) RETURNING id",
            (nome, email),
        )
        user_id = cursor.fetchone()[0]
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()
    return user_id


def list_usuarios():
        connection = get_connection()
        cursor = connection.cursor(cursor_factory = RealDictCursor)
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        cursor.close()
        connection.close()
        return usuarios

def get_usuario_by_id(user_id: int):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM usuario WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    connection.close()
    return usuario

def update_usuario(user_id: int, nome: str = None, email: str = None):
    connection = get_connection()
    cursor = connection.cursor()
    fields = []
    values = []
    
    if nome:
        fields.append("nome = %s")
        values.append(nome)
    if email:
        fields.append("email = %s")
        values.append(email)
    
    values.append(user_id)  # Add user_id for the WHERE clause
    
    if fields:
        query = f"UPDATE usuario SET {', '.join(fields)} WHERE id = %s"
        cursor.execute(query, tuple(values))
        connection.commit()
    
    cursor.close()
    connection.close()

def delete_usuario(user_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM usuario WHERE id = %s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()