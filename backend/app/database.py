from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import get_settings

settings = get_settings()

# Création de l'engine SQLAlchemy
engine = create_engine(
    settings.database_url,
    echo=True,          # affiche les requêtes SQL dans la console (pratique en dev)
    future=True,        # API moderne de SQLAlchemy
)

# Session locale, utilisée dans les endpoints via la dépendance get_db
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base pour déclarer tes modèles SQLAlchemy
class Base(DeclarativeBase):
    pass


# Dépendance FastAPI pour avoir une session DB par requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
