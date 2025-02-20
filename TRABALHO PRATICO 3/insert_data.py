from config import db, clientes_collection, vendas_collection, categorias_collection, plataformas_collection, jogos_collection
from models import Cliente, Venda, Categoria, Plataforma, Jogo
from datetime import datetime

# Inserir um cliente
cliente = Cliente(nome="João Silva", telefone="99999-9999", data_nascimento="1990-05-21", email="joao@email.com")
clientes_collection.insert_one(cliente.dict(by_alias=True))

# Inserir uma categoria
categoria = Categoria(nome="Ação", descricao="Jogos de ação", data_de_criacao=datetime.utcnow(), jogos_associados=[])
categorias_collection.insert_one(categoria.dict(by_alias=True))

# Inserir uma plataforma
plataforma = Plataforma(nome="PlayStation 5", fabricante="Sony", tipo="Console", suporte_online=True)
plataformas_collection.insert_one(plataforma.dict(by_alias=True))

# Inserir um jogo
jogo = Jogo(
    nome="The Last of Us",
    desenvolvedor="Naughty Dog",
    estoque=50,
    preco=199.99,
    data_lancamento="2020-06-19",
    categoria_id=categoria.id,
    plataforma_id=plataforma.id
)
jogos_collection.insert_one(jogo.dict(by_alias=True))

# Inserir uma venda
venda = Venda(
    data=datetime.utcnow(),
    valor_total=199.99,
    forma_pagamento="Cartão de Crédito",
    desconto=0.0,
    cliente_id=cliente.id,
    jogos=[jogo.id]
)
vendas_collection.insert_one(venda.dict(by_alias=True))

print("Dados inseridos com sucesso!")
