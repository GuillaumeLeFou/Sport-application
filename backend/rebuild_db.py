from app.database import Base, engine
import app.models  # IMPORTANT: importe tous les modèles (User, Exercise, etc + stats)

def main():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()