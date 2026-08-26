from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ================================ #
# Chargement des variables d'environnement
# ================================ #

# Rend accessibles les informations de.env.
load_dotenv()


# ================================ #
# Configuration de la connexion
# ================================ #

# Construit l'adresse de connexion
database_url = URL.create(
    # Indique à SQLAlchemy d'utiliser PostgreSQL avec le pilote psycopg
    drivername="postgresql+psycopg",
    # Récupère les informations de connexion dans .env.
    username=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    host=getenv("DB_HOST"),
    port=int(getenv("DB_PORT", "5432")),
    database=getenv("DB_NAME"),
)


# ================================ #
# Création du moteur SQLAlchemy
# ================================ #

# L'engine fait la communication entre SQLAlchemy et PostgreSQL
engine = create_engine(database_url)


# ================================ #
# Base commune des modèles
# ================================ #


class Base(DeclarativeBase):
    pass


# ================================ #
# Création des sessions
# ================================ #

# Permet d'ouvrir les sessions reliées à PostgreSQL
SessionLocale = sessionmaker(bind=engine)
