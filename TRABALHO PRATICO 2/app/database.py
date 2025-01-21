from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Criar o motor de conexão
engine = create_engine(settings.DATABASE_URL, echo=True)

# Sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def init_db():
    """Inicializa o banco de dados criando todas as tabelas definidas no modelo."""
    from app.models import Categoria, Plataforma, Jogo, Cliente, Venda  # Certifique-se de importar todos os modelos
    Base.metadata.create_all(bind=engine)

# Função para obter uma sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
