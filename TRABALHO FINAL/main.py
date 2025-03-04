from fastapi import FastAPI
from routes import deputados, votacoes, orgaos, proposicoes, partidos
from logger import logger  

# Criando a aplicação
app = FastAPI(title="API Câmara dos Deputados", version="1.0")

# Log inicial quando a aplicação inicia
logger.info("API da Câmara dos Deputados iniciada!")

# Incluindo as rotas
app.include_router(deputados.router, prefix="/deputados", tags=["Deputados"])
app.include_router(votacoes.router, prefix="/votacoes", tags=["Votações"])
app.include_router(orgaos.router, prefix="/orgaos", tags=["Órgãos"])
app.include_router(proposicoes.router, prefix="/proposicoes", tags=["Proposições"])
app.include_router(partidos.router, prefix="/partidos", tags=["Partidos"])

@app.get("/")
def read_root():
    logger.info("Rota raiz acessada.")
    return {"message": "API para análise dos dados da Câmara dos Deputados"}


#RELACIONAMENTOS

# 1:N (Partido e Deputados): Um partido tem vários deputados, mas um deputado pertence a um único partido.

# N:N (Deputados e Votações): Deputados podem participar de várias votações, e uma votação pode ter vários deputados.
