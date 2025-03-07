from pymongo import MongoClient

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Conectar ao MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# Criar banco de dados e coleção
db = client["camara_dados"]
deputados_collection = db["deputados"]
colecao_votacoes = db["votacoes"]
partidos_collection = db["partidos"]
