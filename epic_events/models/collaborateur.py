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
    # Nom de la table en DB
    __tablename__ = "collaborateurs"

    # ================================ #
    # Champs obligatoires
    # ================================ #

    # N° employé et ID unique
    numero_employe: Mapped[int] = mapped_column(primary_key=True)

    # Informations sur le collaborateur
    nom: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Hash du mdp
    mot_de_passe_hash: Mapped[str] = mapped_column(String, nullable=False)

    # ID de département associé
    departement_id: Mapped[int] = mapped_column(
        ForeignKey("departements.id"), nullable=False
    )

    # ================================ #
    # Relations
    # ================================ #

    # Accès Département depuis l'objet Python
    departement = relationship("Departement", back_populates="collaborateurs")

    # Accès aux clients associés à leurs commerciaux
    clients = relationship("Client", back_populates="commercial")
