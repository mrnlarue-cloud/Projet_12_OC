from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base

# ================================ #
# Modèle métier d'Événement
# ================================ #


class Evenement(Base):
    # Nom table en DB
    __tablename__ = "evenements"

    # ================================ #
    # Champs obligatoires
    # ================================ #

    # ID unique
    id: Mapped[int] = mapped_column(primary_key=True)

    # Infos de l'événement
    nom: Mapped[str] = mapped_column(String, nullable=False)
    date_debut: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    lieu: Mapped[str] = mapped_column(String, nullable=False)
    nombre_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=False)

    # ================================ #
    # Relations
    # ================================ #

    # ID unique du contrat associé
    contrat_id: Mapped[int] = mapped_column(
        ForeignKey("contrats.id"), unique=True, nullable=False
    )

    # ID facultatif du collaborateur support
    support_id: Mapped[int | None] = mapped_column(
        ForeignKey("collaborateurs.numero_employe"), nullable=True
    )

    # Accès au contrat et au support depuis l'objet Python
    contrat = relationship("Contrat", back_populates="evenement")
    support = relationship("Collaborateur", back_populates="evenements")
