# Charge la base commune et la connexion PostgreSQL
from epic_events.database import Base, engine

# Charge les modèles pour enregistrer leurs tables dans SQLAlchemy
from epic_events.models.clients import Client
from epic_events.models.collaborateur import Collaborateur
from epic_events.models.contrats import Contrat
from epic_events.models.departement import Departement
from epic_events.models.evenements import Evenement

# ================================ #
# Création des tables
# ================================ #


def creation_tables():
    # Vérifie toutes les tables nécessaires à l'application
    # Crée les tables absentes
    Base.metadata.create_all(
        bind=engine,
        tables=[
            Departement.__table__,
            Collaborateur.__table__,
            Client.__table__,
            Contrat.__table__,
            Evenement.__table__,
        ],
    )

    # Confirme la fin de la création
    print("Tables PostgreSQL créées ou déjà présentes.")


# Lance la création uniquement si ce fichier est exécuté directement
if __name__ == "__main__":
    creation_tables()
