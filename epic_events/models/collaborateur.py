# Indique que la colonne PostgreSQL stocke du texte
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

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
