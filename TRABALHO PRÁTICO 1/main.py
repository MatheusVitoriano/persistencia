from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Produto(BaseModel):
    id: int = Field(..., gt=0, description="ID único do produto, deve ser maior que 0")
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do produto")
    categoria: str = Field(..., min_length=1, max_length=50, description="Categoria do produto")
    preco: float = Field(..., gt=0, description="Preço do produto, deve ser maior que 0")
    data_criacao: Optional[date] = Field(default_factory=date.today, description="Data de criação do produto")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nome": "Chocolate Amargo",
                "categoria": "Alimentos",
                "preco": 25.50,
                "data_criacao": "29/11/2024"
            }
        }

# Exemplo de uso
produto_exemplo = Produto(id=1, nome="Ovo de Páscoa Gourmet", categoria="Doces", preco=49.90)

# Exibindo a data formatada
print(f"Produto: {produto_exemplo.nome}")
print(f"Data de criação formatada: {produto_exemplo.data_criacao.strftime('%Y/%m/%d')}")
