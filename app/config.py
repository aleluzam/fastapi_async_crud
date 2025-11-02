from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:1234@localhost:5432/fastapi_db"
    secret_key: str 
    algorithm: str = "HS256"   
    
    model_config = SettingsConfigDict(
        env_file= ".env",
        case_sensitive = False
    )

settings = Settings()