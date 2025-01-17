from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:123456@localhost:5432/meu_projeto"

    class Config:
        env_file = ".env"

# Instância única de configuração
settings = Settings()
