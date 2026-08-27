from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base

# ================================
# Modèle métier de Client
# ================================


class Client(Base):
    # Nom de la table en DB
    __tablename__ = "clients"

    # ================================ #
    # Champs obligatoires
    # ================================ #

    # ID unique
    id: Mapped[int] = mapped_column(primary_key=True)

    # Info du client
    nom_complet: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    telephone: Mapped[str] = mapped_column(String, nullable=False)
    entreprise: Mapped[str] = mapped_column(String, nullable=False)
    date_creation_contact: Mapped[date] = mapped_column(Date, nullable=False)
    date_dernier_echange: Mapped[date] = mapped_column(Date, nullable=False)

    # ID du commercial responsable du client
    commercial_id: Mapped[int] = mapped_column(
        ForeignKey("collaborateurs.numero_employe"), nullable=False
    )

    # ================================ #
    # Relations
    # ================================ #

    # Accès au commercial depuis l'objet Python
    commercial = relationship("Collaborateur", back_populates="clients")

    # Accès aux contrats associés au client
    contrats = relationship("Contrat", back_populates="client")
