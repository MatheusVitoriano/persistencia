from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from bson import ObjectId
from typing import List
from datetime import datetime

#Clientes
class Cliente(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome: str
    telefone: str
    data_nascimento: datetime
    email: EmailStr

#Vendas
class Venda(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    data: datetime
    valor_total: float
    forma_pagamento: str
    desconto: float
    cliente_id: str  # Referencia um cliente
    jogos: List[str]  # Lista de IDs de jogos comprados

#Categorias
class Categoria(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome: str
    descricao: str
    data_de_criacao: datetime
    jogos_associados: List[str]  # IDs dos jogos dessa categoria

#Plataformas
class Plataforma(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome: str
    fabricante: str
    tipo: str  # Ex: Console, PC, Mobile
    suporte_online: bool

#Jogos
class Jogo(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome: str
    desenvolvedor: str
    estoque: int
    preco: float
    data_lancamento: datetime
    categoria_id: str  # Referência a uma categoria
    plataforma_id: str  # Referência a uma plataforma

# 1 categoria para 1 jogo
# 1 jogo para 1 categoria

# 1 cliente para N jogos

