from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xml.etree.ElementTree as ET
import os

app = FastAPI()

# Rota raiz
@app.get("/")
def raiz():
    return {"mensagem": "Está funcionando"}

# Nome do arquivo XML
ARQUIVO_XML = "livros.xml"

# Modelo para validação de dados
class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    ano: int
    genero: str

# Função para carregar os dados do XML
def carregar_livros():
    if not os.path.exists(ARQUIVO_XML):
        criar_arquivo_xml_vazio()
    tree = ET.parse(ARQUIVO_XML)
    root = tree.getroot()
    livros = []
    for livro_elem in root.findall("livro"):
        livros.append({
            "id": int(livro_elem.find("id").text),
            "titulo": livro_elem.find("titulo").text,
            "autor": livro_elem.find("autor").text,
            "ano": int(livro_elem.find("ano").text),
            "genero": livro_elem.find("genero").text,
        })
    return livros

# Função para salvar os dados no XML
def salvar_livros(livros):
    root = ET.Element("livros")
    for livro in livros:
        livro_elem = ET.Element("livro")
        for chave, valor in livro.items():
            campo = ET.Element(chave)
            campo.text = str(valor)
            livro_elem.append(campo)
        root.append(livro_elem)
    tree = ET.ElementTree(root)
    tree.write(ARQUIVO_XML)

# Criar arquivo XML vazio se não existir
def criar_arquivo_xml_vazio():
    root = ET.Element("livros")
    tree = ET.ElementTree(root)
    tree.write(ARQUIVO_XML)

# Rota para criar um livro
@app.post("/livros", status_code=201)
def criar_livro(livro: Livro):
    livros = carregar_livros()
    if any(l["id"] == livro.id for l in livros):
        raise HTTPException(status_code=400, detail="ID já existe.")
    livros.append(livro.dict())
    salvar_livros(livros)
    return livro

# Rota para listar todos os livros
@app.get("/livros")
def listar_livros():
    livros = carregar_livros()
    return livros

# Rota para buscar livro por ID
@app.get("/livros/{id}")
def buscar_livro(id: int):
    livros = carregar_livros()
    for livro in livros:
        if livro["id"] == id:
            return livro
    raise HTTPException(status_code=404, detail="Livro não encontrado.")

# Rota para atualizar livro
@app.put("/livros/{id}")
def atualizar_livro(id: int, livro_atualizado: Livro):
    livros = carregar_livros()
    for i, livro in enumerate(livros):
        if livro["id"] == id:
            livros[i] = livro_atualizado.dict()
            salvar_livros(livros)
            return livro_atualizado
    raise HTTPException(status_code=404, detail="Livro não encontrado.")

# Rota para deletar livro
@app.delete("/livros/{id}")
def deletar_livro(id: int):
    livros = carregar_livros()
    for i, livro in enumerate(livros):
        if livro["id"] == id:
            del livros[i]
            salvar_livros(livros)
            return {"mensagem": "Livro deletado com sucesso."}
    raise HTTPException(status_code=404, detail="Livro não encontrado.")
