from app.database import SessionLocal
from app.models import Categoria, Plataforma, Jogo, Cliente, Venda

db = SessionLocal()

# Inserir Categorias
categoria1 = Categoria(nome="Ação", descricao="Jogos de ação", data_criacao="2023-01-01", ativo=True)
categoria2 = Categoria(nome="RPG", descricao="Jogos de RPG", data_criacao="2023-01-02", ativo=True)

# Inserir Plataformas
plataforma1 = Plataforma(nome="PC", fabricante="Microsoft", suporte_online=True, tipo="Desktop")
plataforma2 = Plataforma(nome="PlayStation", fabricante="Sony", suporte_online=True, tipo="Console")

# Inserir Jogos
jogo1 = Jogo(nome="Jogo A", desenvolvedor="Dev A", preco=59.99, estoque=100, data_lancamento="2023-06-01")
jogo2 = Jogo(nome="Jogo B", desenvolvedor="Dev B", preco=89.99, estoque=50, data_lancamento="2023-07-01")

# Relacionar Jogos com Categorias e Plataformas
jogo1.categorias.append(categoria1)
jogo1.plataformas.append(plataforma1)

jogo2.categorias.append(categoria2)
jogo2.plataformas.append(plataforma2)

# Inserir Cliente
cliente = Cliente(nome="João Silva", telefone="123456789", email="joao@gmail.com", data_nascimento="1990-05-20")

# Inserir Venda
venda = Venda(cliente=cliente, valor=59.99, desconto=5.00, data_venda="2023-07-10", jogo=jogo1)

# Adicionar ao banco
db.add_all([categoria1, categoria2, plataforma1, plataforma2, jogo1, jogo2, cliente, venda])
db.commit()

print("Dados inseridos com sucesso!")
