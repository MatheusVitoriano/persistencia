from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Conectar ao MongoDB
try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)  
    db = client["loja_jogos"]

    # Criar coleções
    clientes_collection = db["clientes"]
    vendas_collection = db["vendas"]
    categorias_collection = db["categorias"]
    plataformas_collection = db["plataformas"]
    jogos_collection = db["jogos"]

    # Criar índices para otimizar buscas
    clientes_collection.create_index("email", unique=True)
    vendas_collection.create_index("cliente_id")
    jogos_collection.create_index("categoria_id")
    jogos_collection.create_index("plataforma_id")

    # Testar a conexão
    client.server_info()
    print("Conectado ao MongoDB!")

except ConnectionFailure as e:
    print(f"Erro ao conectar ao MongoDB: {e}")

# Exportar o banco e coleções
def get_database():
    return db

# Exportar coleções
__all__ = ["db", "clientes_collection", "vendas_collection", "categorias_collection", "plataformas_collection", "jogos_collection"]
