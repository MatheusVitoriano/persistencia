from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabela associativa para muitos-para-muitos entre Jogos e Vendas
jogo_venda_associacao = Table(
    "jogos_vendas",
    Base.metadata,
    Column("jogo_id", Integer, ForeignKey("jogos.id", ondelete="CASCADE"), primary_key=True),
    Column("venda_id", Integer, ForeignKey("vendas.id", ondelete="CASCADE"), primary_key=True),
)

# Entidade Categoria
class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)
    data_criacao = Column(Date, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamento bidirecional com Jogo
    jogos = relationship("Jogo", back_populates="categoria", cascade="all, delete-orphan")


# Entidade Plataforma
class Plataforma(Base):
    __tablename__ = "plataformas"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(100), nullable=False)
    fabricante = Column(String(100), nullable=False)
    suporte_online = Column(Boolean, default=False, nullable=False)
    tipo = Column(String(50), nullable=False)

    # Relacionamento bidirecional com Jogo
    jogos = relationship("Jogo", back_populates="plataforma", cascade="all, delete-orphan")


# Entidade Desenvolvedor
class Desenvolvedor(Base):
    __tablename__ = "desenvolvedores"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(100), nullable=False)
    pais_origem = Column(String(100), nullable=True)

    # Relacionamento 1:1 com Jogo
    jogo = relationship("Jogo", back_populates="desenvolvedor", uselist=False, cascade="all, delete-orphan")


# Entidade Cliente
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(150), nullable=False)
    telefone = Column(String(20), nullable=True)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)

    # Relacionamento bidirecional com Venda
    vendas = relationship("Venda", back_populates="cliente", cascade="all, delete-orphan")


# Entidade Venda
class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    desconto = Column(Float, nullable=False)
    data_venda = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    forma_de_pagamento = Column(String(50), nullable=False)

    # Relacionamento com Cliente
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    cliente = relationship("Cliente", back_populates="vendas")

    # Relacionamento bidirecional com Jogo (muitos para muitos)
    jogos = relationship("Jogo", secondary=jogo_venda_associacao, back_populates="vendas")


# Entidade Jogo
class Jogo(Base):
    __tablename__ = "jogos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(150), nullable=False)
    estoque = Column(Integer, default=0, nullable=False)
    preco = Column(Float, nullable=False)
    data_lancamento = Column(Date, nullable=False)

    # Relacionamento com Categoria (1:N)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True, index=True)
    categoria = relationship("Categoria", back_populates="jogos")

    # Relacionamento com Plataforma (1:N)
    plataforma_id = Column(Integer, ForeignKey("plataformas.id", ondelete="SET NULL"), nullable=True, index=True)
    plataforma = relationship("Plataforma", back_populates="jogos")

    # Relacionamento com Desenvolvedor (1:1)
    desenvolvedor_id = Column(Integer, ForeignKey("desenvolvedores.id", ondelete="CASCADE"), unique=True, nullable=True)
    desenvolvedor = relationship("Desenvolvedor", back_populates="jogo")

    # Relacionamento com Venda (N:N)
    vendas = relationship("Venda", secondary=jogo_venda_associacao, back_populates="jogos")
