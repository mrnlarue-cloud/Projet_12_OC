# SQLAlchemy pour les textes en BDD
from sqlalchemy import String

# Mapped = type Python, mapped_column = colonne SQL
from sqlalchemy.orm import Mapped, mapped_column

# Base commune aux modèles
from epic_events.database import Base

# ================================ #
# Modèle métier pour Département
# ================================ #


class Departement(Base):
    # Nom de la table en BDD
    __tablename__ = "departements"

    # ID unique
    id: Mapped[int] = mapped_column(primary_key=True)

    # Nom obligatoire et unique
    nom: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
