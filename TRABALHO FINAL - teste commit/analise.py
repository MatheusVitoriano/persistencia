import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient

router = APIRouter()

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["camara_dados"]
deputados_collection = db["deputados"]

# Criar pasta para armazenar imagens
IMAGES_DIR = "static/images"
os.makedirs(IMAGES_DIR, exist_ok=True)

@router.get("/estatisticas/grafico-deputados-por-partido")
def gerar_grafico_deputados_por_partido():
  
    try:
        # Obter dados do MongoDB
        pipeline = [
            {"$group": {"_id": "$siglaPartido", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}}
        ]
        resultado = list(deputados_collection.aggregate(pipeline))

        if not resultado:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")

        # Converter para DataFrame
        df = pd.DataFrame(resultado)
        df.columns = ["Partido", "Deputados"]

        # Criar gráfico
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Deputados", y="Partido", data=df, hue="Partido", palette="viridis", legend=False)
        plt.xlabel("Número de Deputados")
        plt.ylabel("Partido")
        plt.title("Quantidade de Deputados por Partido")

        # Salvar a imagem
        image_path = os.path.join(IMAGES_DIR, "deputados_por_partido.png")
        plt.savefig(image_path, bbox_inches="tight")
        plt.close()

        return {"message": "Gráfico gerado com sucesso", "image_url": f"/{image_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")

@router.get("/estatisticas/grafico-deputados-por-estado")
def gerar_grafico_deputados_por_estado():
   
    try:
        # Obter dados do MongoDB
        pipeline = [
            {"$group": {"_id": "$siglaUf", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}}
        ]
        resultado = list(deputados_collection.aggregate(pipeline))

        if not resultado:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado")

        # Converter para DataFrame
        df = pd.DataFrame(resultado)
        df.columns = ["Estado", "Deputados"]

        # Criar gráfico
        plt.figure(figsize=(12, 6))
        sns.barplot(x="Deputados", y="Estado", data=df, hue="Estado", palette="magma", legend=False)
        plt.xlabel("Número de Deputados")
        plt.ylabel("Estado (UF)")
        plt.title("Quantidade de Deputados por Estado")

        # Salvar a imagem
        image_path = os.path.join(IMAGES_DIR, "deputados_por_estado.png")
        plt.savefig(image_path, bbox_inches="tight")
        plt.close()

        return {"message": "Gráfico gerado com sucesso", "image_url": f"/{image_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar gráfico: {str(e)}")
