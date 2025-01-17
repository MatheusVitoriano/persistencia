# Inserir CATEGORIAS

from app.models import Categoria, session

# Criar categorias
categorias = [
    Categoria(nome="Ação", descricao="Jogos de ação e aventura", data_criacao=date(2023, 1, 1), ativo=True),
    Categoria(nome="RPG", descricao="Jogos de interpretação de papéis", data_criacao=date(2022, 12, 9), ativo=True),
    Categoria(nome="Esportes", descricao="Jogos esportivos e competições", data_criacao=date, ativo=True),
]

# Adicionar ao banco de dados, evitando duplicatas
for categoria in categorias:
    if not session.query(Categoria).filter_by(nome=categoria.nome).first():
        session.add(categoria)

session.commit()
print("Categorias inseridas com sucesso!")

# Inserir JOGOS

from app.models import Jogo, session
from datetime import date

# Criar jogos
jogos = [
    Jogo(nome="Jogo Ação 1", desenvolvedor="Dev Ação", preco=59.99, estoque=10, data_lancamento=date(2023, 11, 1)),
    Jogo(nome="Jogo RPG 1", desenvolvedor="Dev RPG", preco=89.99, estoque=5, data_lancamento=date(2022, 5, 15)),
    Jogo(nome="Jogo Esporte 1", desenvolvedor="Dev Esportes", preco=49.99, estoque=20, data_lancamento=date(2021, 7, 20)),
]

# Adicionar ao banco de dados, evitando duplicatas
for jogo in jogos:
    if not session.query(Jogo).filter_by(nome=jogo.nome).first():
        session.add(jogo)

session.commit()
print("Jogos inseridos com sucesso!")

# Inserir CLIENTES

from app.models import Cliente, session
from datetime import date

# Criar clientes
clientes = [
    Cliente(nome="João Silva", telefone="123456789", data_nascimento=date(1990, 1, 15), email="joao@email.com"),
    Cliente(nome="Maria Oliveira", telefone="987654321", data_nascimento=date(1995, 6, 30), email="maria@email.com"),
    Cliente(nome="Pedro Santos", telefone="555555555", data_nascimento=date(1988, 3, 10), email="pedro@email.com"),
]

# Adicionar ao banco de dados, evitando duplicatas
for cliente in clientes:
    if not session.query(Cliente).filter_by(email=cliente.email).first():
        session.add(cliente)

session.commit()
print("Clientes inseridos com sucesso!")

# Testar RELACIONAMENTO JOGOS E CATEGORIAS

from app.models import session, JogoCategoria

# Relacionar jogos às categorias (IDs devem ser válidos no banco)
relacionamentos = [
    JogoCategoria(jogo_id=1, categoria_id=1),  # Jogo Ação 1 -> Categoria Ação
    JogoCategoria(jogo_id=2, categoria_id=2),  # Jogo RPG 1 -> Categoria RPG
    JogoCategoria(jogo_id=3, categoria_id=3),  # Jogo Esporte 1 -> Categoria Esportes
]

# Adicionar ao banco, evitando duplicatas
for relacionamento in relacionamentos:
    if not session.query(JogoCategoria).filter_by(jogo_id=relacionamento.jogo_id, categoria_id=relacionamento.categoria_id).first():
        session.add(relacionamento)

session.commit()
print("Relacionamentos entre jogos e categorias inseridos com sucesso!")

# Inserir VENDAS

from app.models import Venda, session
from datetime import date

# Criar vendas
vendas = [
    Venda(cliente_id=1, desconto=10.0, valor=49.99, data_venda=date(2025, 1, 14)),
    Venda(cliente_id=2, desconto=5.0, valor=84.99, data_venda=date(2025, 1, 14)),
]

# Adicionar ao banco, evitando duplicatas
for venda in vendas:
    if not session.query(Venda).filter_by(cliente_id=venda.cliente_id, data_venda=venda.data_venda).first():
        session.add(venda)

session.commit()
print("Vendas inseridas com sucesso!")

# Consultar JOGOS

jogos = session.query(Jogo).all()
for jogo in jogos:
    print(jogo.nome, jogo.preco)

# Consultar CLIENTES

clientes = session.query(Cliente).all()
for cliente in clientes:
    print(cliente.nome, cliente.email)

# Consultar VENDAS

clientes = session.query(Cliente).all()
for cliente in clientes:
    print(cliente.nome, cliente.email)
