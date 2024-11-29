from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import os
import zipfile
from fastapi.responses import FileResponse

app = FastAPI()

# Nome do arquivo CSV
ARQUIVO_CSV = "produtos.csv"
ARQUIVO_ZIP = "produtos.zip"

# Modelo para validação de dados
class Produto(BaseModel):
    id: int
    nome: str
    categoria: str
    preco: float
    data_criacao: str

# Função para carregar os dados do CSV
def carregar_produtos():
    if not os.path.exists(ARQUIVO_CSV):
        criar_arquivo_csv_vazio()
    produtos = []
    with open(ARQUIVO_CSV, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            produtos.append({
                "id": int(row["id"]),
                "nome": row["nome"],
                "categoria": row["categoria"],
                "preco": float(row["preco"]),
                "data_criacao": row["data_criacao"],
            })
    return produtos

# Função para salvar os dados no CSV
def salvar_produtos(produtos):
    with open(ARQUIVO_CSV, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["id", "nome", "categoria", "preco", "data_criacao"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto)

# Criar arquivo CSV vazio se não existir
def criar_arquivo_csv_vazio():
    with open(ARQUIVO_CSV, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["id", "nome", "categoria", "preco", "data_criacao"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

# Rota raiz para verificar se o servidor está funcionando
@app.get("/")
def raiz():
    return {"mensagem": "API de Produtos está funcionando!"}

# Rota para criar um produto
@app.post("/produtos", status_code=201)
def criar_produto(produto: Produto):
    produtos = carregar_produtos()
    
    # Verificar se o ID já existe
    if any(p["id"] == produto.id for p in produtos):
        raise HTTPException(status_code=400, detail="ID já existe.")
    
    # Adicionar novo produto à lista
    produtos.append(produto.dict())
    
    # Salvar a lista atualizada no CSV
    salvar_produtos(produtos)
    return produto

# Rota para listar todos os produtos
@app.get("/produtos")
def listar_produtos():
    produtos = carregar_produtos()
    return produtos

# Rota para buscar produto por ID
@app.get("/produtos/{id}")
def buscar_produto(id: int):
    produtos = carregar_produtos()
    for produto in produtos:
        if produto["id"] == id:
            return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado.")

# Rota para atualizar produto
@app.put("/produtos/{id}")
def atualizar_produto(id: int, produto_atualizado: Produto):
    produtos = carregar_produtos()
    
    # Buscar o índice do produto para atualizar
    for i, produto in enumerate(produtos):
        if produto["id"] == id:
            produtos[i] = produto_atualizado.dict()
            salvar_produtos(produtos)
            return produto_atualizado
    
    raise HTTPException(status_code=404, detail="Produto não encontrado.")

# Rota para deletar produto
@app.delete("/produtos/{id}")
def deletar_produto(id: int):
    produtos = carregar_produtos()
    
    # Buscar o índice do produto para deletar
    for i, produto in enumerate(produtos):
        if produto["id"] == id:
            del produtos[i]
            salvar_produtos(produtos)
            return {"mensagem": "Produto deletado com sucesso."}
    
    raise HTTPException(status_code=404, detail="Produto não encontrado.")

# Rota para mostrar a quantidade de produtos cadastrados
@app.get("/produtos/mostrar/quantidades")
def contar_produtos():
    produtos = carregar_produtos()
    quantidade = len(produtos)
    return {"quantidade": quantidade}

# Rota para compactar o arquivo CSV em um arquivo ZIP
@app.get("/produtos/arquivo/compactar")
def compactar_csv_em_zip():
    # Verificar se o arquivo CSV existe
    if not os.path.exists(ARQUIVO_CSV):
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado.")
    
    # Criar o arquivo ZIP
    with zipfile.ZipFile(ARQUIVO_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(ARQUIVO_CSV, os.path.basename(ARQUIVO_CSV))

    # Retornar o arquivo ZIP para download
    return FileResponse(ARQUIVO_ZIP, media_type='application/zip', filename=ARQUIVO_ZIP)
