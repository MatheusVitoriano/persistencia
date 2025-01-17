from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.logging_config import get_logger

from app.routes.jogo_routes import router as jogo_router
from app.routes.categoria_routes import router as categoria_router
from app.routes.cliente_routes import router as cliente_router
from app.routes.venda_routes import router as venda_router
from app.routes.plataforma_routes import router as plataforma_router

# Configurar o logger
logger = get_logger("MainApp")

# Criar a aplicação FastAPI
app = FastAPI(
    title="Gerenciador de Jogos",
    description="API para gerenciar jogos, categorias, clientes e vendas",
    version="1.0.0",
)

# Função para inicializar o banco de dados
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")

# Incluir as rotas
app.include_router(jogo_router, prefix="/api", tags=["Jogos"])
app.include_router(categoria_router, prefix="/api", tags=["Categorias"])
app.include_router(cliente_router, prefix="/api", tags=["Clientes"])
app.include_router(venda_router, prefix="/api", tags=["Vendas"])
app.include_router(plataforma_router, prefix="/api", tags=["Plataformas"])

# Evento de inicialização da aplicação
@app.on_event("startup")
def startup_event():
    logger.info("Inicializando aplicação")
    init_db()
    logger.info("Aplicação inicializada com sucesso")

# Rota principal para verificar se a API está funcionando
@app.get("/")
async def read_root():
    return {"message": "API está funcionando!"}
