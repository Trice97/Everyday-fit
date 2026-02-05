from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from app.config import settings

#Création du moteur de connexion à PostgreSQL
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

#Création de la session locale (pour interagir avec de la DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de classe pour les modèles SQLalchemy
Base = declarative_base()
