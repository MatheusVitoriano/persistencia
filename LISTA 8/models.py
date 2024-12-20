from pydantic import  BaseModel
from typing import List

class Usuario (BaseModel):
    id: int
    name: str
    email: str


class Pedido (BaseModel):
    id: int
    usuario_id: int
    data_pedido: str
    status: str


class Produto (BaseModel):
    id: int
    pedido_id: int
    nome: str
    preco: float
    quantidade: int

class pedido_produto(BaseModel):
    id: int
    pedido_id: int
    quantidade: int