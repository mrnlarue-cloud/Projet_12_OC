from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base

# ================================ #
# Modèle métier de Contrat
# ================================ #


class Contrat(Base):
    # Nom de la table en DB
    __tablename__ = "contrats"

    # ================================ #
    # Champs obligatoires
    # ================================ #

    # ID unique
    id: Mapped[int] = mapped_column(primary_key=True)

    # Infos du contrat
    montant_total: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    montant_restant: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    date_creation: Mapped[date] = mapped_column(Date, nullable=False)
    signature: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # ================================ #
    # Relations
    # ================================ #

    # IDs du client et du commercial associés
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    commercial_id: Mapped[int] = mapped_column(
        ForeignKey("collaborateurs.numero_employe"), nullable=False
    )
    # Accès au client & commercial depuis l'objet python
    client = relationship("Client", back_populates="contrats")
    commercial = relationship("Collaborateur", back_populates="contrats")
