from fastapi import FastAPI
from routes.clientes import router as clientes_router
from routes.vendas import router as vendas_router
from routes.categorias import router as categorias_router
from routes.plataformas import router as plataformas_router
from routes.jogos import router as jogos_router

app = FastAPI()

app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(vendas_router, prefix="/vendas", tags=["Vendas"])
app.include_router(categorias_router, prefix="/categorias", tags=["Categorias"])
app.include_router(plataformas_router, prefix="/plataformas", tags=["Plataformas"])
app.include_router(jogos_router, prefix="/jogos", tags=["Jogos"])
