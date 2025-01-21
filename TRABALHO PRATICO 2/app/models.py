from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Tabela de associação N:N entre Jogos e Categorias
jogo_categoria_associacao = Table(
    'jogo_categoria',
    Base.metadata,
    Column('jogo_id', Integer, ForeignKey('jogos.id'), primary_key=True),
    Column('categoria_id', Integer, ForeignKey('categorias.id'), primary_key=True)
)

# Tabela de associação N:N entre Jogos e Plataformas
jogo_plataforma_associacao = Table(
    'jogo_plataforma',
    Base.metadata,
    Column('jogo_id', Integer, ForeignKey('jogos.id'), primary_key=True),
    Column('plataforma_id', Integer, ForeignKey('plataformas.id'), primary_key=True)
)


class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data_criacao = Column(Date, nullable=False)
    ativo = Column(Boolean, default=True)

    # Relacionamento com Jogos
    jogos = relationship(
        "Jogo",
        secondary=jogo_categoria_associacao,
        back_populates="categorias"
    )


class Plataforma(Base):
    __tablename__ = 'plataformas'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    fabricante = Column(String, nullable=False)
    suporte_online = Column(Boolean, default=False)
    tipo = Column(String, nullable=False)

    # Relacionamento com Jogos
    jogos = relationship(
        "Jogo",
        secondary=jogo_plataforma_associacao,
        back_populates="plataformas"
    )


class Jogo(Base):
    __tablename__ = 'jogos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    desenvolvedor = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    data_lancamento = Column(Date, nullable=False)

    # Relacionamento com Categorias
    categorias = relationship(
        "Categoria",
        secondary=jogo_categoria_associacao,
        back_populates="jogos"
    )

    # Relacionamento com Plataformas
    plataformas = relationship(
        "Plataforma",
        secondary=jogo_plataforma_associacao,
        back_populates="jogos"
    )


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String)
    data_nascimento = Column(Date)
    email = Column(String, unique=True, index=True)

    # Relacionamento com Vendas
    vendas = relationship("Venda", back_populates="cliente")


class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    desconto = Column(Float)
    valor = Column(Float, nullable=False)
    data_venda = Column(Date, nullable=False)

    # Relacionamento com Cliente
    cliente = relationship("Cliente", back_populates="vendas")




