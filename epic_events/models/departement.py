# Indique que la colonne PostgreSQL stocke du texte
from sqlalchemy import String

# Mapped = type Python, mapped_column = colonne SQL
# relationship = lien entre les objets Python
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base

# ================================ #
# Modèle métier pour Département
# ================================ #


class Departement(Base):
    # Nom de la table en DB
    __tablename__ = "departements"

    # ================================ #
    # Champs obligatoires
    # ================================ #

    # ID unique
    id: Mapped[int] = mapped_column(primary_key=True)

    # Nom obligatoire et unique
    nom: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # ================================ #
    # Relations
    # ================================ #

    # Collaborateurs associés au Département
    collaborateurs = relationship("Collaborateur", back_populates="departement")
