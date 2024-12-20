from fastapi import FastAPI, HTTPException
from crud import list_usuarios, create_usuario
from db import create_tables, get_connection

app = FastAPI()

# Criar tabelas no banco de dados ao iniciar o servidor
create_tables()

# Endpoint para listar todos os usuários
@app.get("/usuarios")
def listar_usuarios():
    try:
        usuarios = list_usuarios()
        return {"usuarios": usuarios}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para criar um novo usuário
@app.post("/usuarios")
def criar_usuario(nome: str, email: str):
    try:
        user_id = create_usuario(nome, email)
        return {"message": "Usuário criado com sucesso", "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
