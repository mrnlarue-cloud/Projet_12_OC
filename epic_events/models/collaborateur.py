# String = texte en BDD, ForeignKey = ID lié à une autre table
from sqlalchemy import ForeignKey, String

# Mapped = type Python, mapped_column = colonne SQL
# relationship = lien entre les objets Python
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base

# ================================ #
# Modèle métier de Collaborateur
# ================================ #


class Collaborateur(Base):
    # Nom de la table en BDD
    __tablename__ = "collaborateurs"

    # N° employé et ID unique
    numero_employe: Mapped[int] = mapped_column(primary_key=True)

    # Informations sur le collaborateur
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Hash du mdp
    mot_de_passe_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # ID de département associé
    departement_id: Mapped[int] = mapped_column(
        ForeignKey("departements.id"), nullable=False
    )

    # Accès Département depuis l'objet Python
    departement = relationship("Departement", back_populates="collaborateurs")
