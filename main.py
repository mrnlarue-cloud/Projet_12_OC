from sqlalchemy import text

from epic_events.database import engine

# ================================ #
# Vérification de la connexion
# ================================ #


def verifier_connexion():
    """Vérifie que l'app communique avec PostgreSQL."""
    with engine.connect() as connexion:
        connexion.execute(text("SELECT 1"))

    print("Connexion à PostgreSQL réussie.")


# ================================ #
# Point d'entrée du programme
# ================================ #


if __name__ == "__main__":
    verifier_connexion()
