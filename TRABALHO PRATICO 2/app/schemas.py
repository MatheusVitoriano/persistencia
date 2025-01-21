from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from typing import Optional
from datetime import datetime



# Modelo Pydantic para Categoria
class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    data_criacao: date
    ativo: bool

# Modelo para leitura (inclui o ID e lista de jogos, se necessário)
class CategoriaRead(CategoriaBase):
    id: int

    class Config:
        orm_mode = True

# Modelo para criação (exclui o ID, que será gerado pelo banco)
class CategoriaCreate(CategoriaBase):
    pass

# Modelo para atualização (todas as propriedades opcionais)
class CategoriaUpdate(BaseModel):
    nome: Optional[str]
    descricao: Optional[str]
    data_criacao: Optional[date]
    ativo: Optional[bool]

    class Config:
        orm_mode = True
#---------------------------------------------------------------------------------------------

class ClienteBase(BaseModel):
    nome: str
    telefone: Optional[str]
    data_nascimento: date
    email: str

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True  # Permite conversão de objetos SQLAlchemy para Pydantic

#---------------------------------------------------------------------------------------------

class VendaBase(BaseModel):
    cliente_id: int
    data_venda: date 
    valor: float
    desconto: float
    forma_de_pagamento: str


class VendaCreate(VendaBase):
    pass

class VendaResponse(VendaBase):
    id: int

    class Config:
        from_attributes = True  # Permite converter modelos SQLAlchemy para Pydantic

#--------------------------------------------------------------------------------------------------

# Modelo Pydantic para Jogo (usado no relacionamento)
class JogoBase(BaseModel):
    id: int
    nome: str;

    class Config:
        from_attributes = True  # Permite conversão de objetos SQLAlchemy para Pydantic


# Modelo base para criação de Plataforma
class PlataformaBase(BaseModel):
    nome: str
    fabricante: str
    suporte_online: Optional[bool] = False
    tipo: str


# Modelo usado para criar uma nova Plataforma
class PlataformaCreate(PlataformaBase):
    pass


# Modelo usado para retornar uma Plataforma completa (inclui jogos)
class PlataformaResponse(PlataformaBase):
    id: int
    jogos: List[JogoBase] = []

    class Config:
        from_attributes = True  # Permite conversão de SQLAlchemy para Pydantic

