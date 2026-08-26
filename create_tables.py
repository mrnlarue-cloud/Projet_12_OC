# Charge tous les modèles dans SQLAlchemy
from epic_events import models
from epic_events.database import Base, engine

# ================================ #
# Création des tables
# ================================ #


def creation_tables():
    # Crée uniquement les tables absentes
    Base.metadata.create_all(bind=engine)

    print(f"Tables PostgreSQL de {models.__name__} créées ou déjà présentes.")


if __name__ == "__main__":
    creation_tables()
