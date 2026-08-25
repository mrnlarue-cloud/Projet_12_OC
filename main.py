from sqlalchemy import text

from epic_events.database import engine


def verifier_connexion():
    with engine.connect() as connexion:
        connexion.execute(text("SELECT 1"))

    print("Connexion à PostgreSQL réussie.")


if __name__ == "__main__":
    verifier_connexion()