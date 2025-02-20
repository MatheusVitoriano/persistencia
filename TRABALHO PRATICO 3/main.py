from fastapi import FastAPI
from routes.clientes import router as clientes_router
from routes.vendas import router as vendas_router
from routes.categorias import router as categorias_router
from routes.plataformas import router as plataformas_router
from routes.jogos import router as jogos_router
from api import app

# 🚀 Executando a API com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

app = FastAPI(title="API de Vendas de Jogos", version="1.0", description="Gerenciamento de clientes, vendas, categorias, plataformas e jogos.")

# 🔗 Adicionando todas as rotas da API
app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(vendas_router, prefix="/vendas", tags=["Vendas"])
app.include_router(categorias_router, prefix="/categorias", tags=["Categorias"])
app.include_router(plataformas_router, prefix="/plataformas", tags=["Plataformas"])
app.include_router(jogos_router, prefix="/jogos", tags=["Jogos"])
