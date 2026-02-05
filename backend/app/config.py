from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuration de l'application chargée depuis .env"""

    #database
    DATABASE_URL: str

    #Security
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    #App 
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
         env_file = ".env"

settings = Settings()
