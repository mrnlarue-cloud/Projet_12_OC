# ================================ #
# Imports
# ================================ #

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base
from epic_events.security.chiffrement import TexteChiffre

# ================================ #
# Modèle métier d'Évènements
# ================================ #


class Evenement(Base):
    # Nom table en DB
    __tablename__ = "evenements"

    # ================================ #
    # Champs obligatoires du modèle Évènements
    # ================================ #

    # ID unique
    id: Mapped[int] = mapped_column(primary_key=True)

    # Infos de l'évènement
    nom: Mapped[str] = mapped_column(TexteChiffre(), nullable=False)
    date_debut: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    lieu: Mapped[str] = mapped_column(TexteChiffre(), nullable=False)
    nombre_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(TexteChiffre(), nullable=False)

    # ================================ #
    # Relations du modèle Évènements
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


# ================================ #
# Conversion des saisies du modèle Évènements
# ================================ #


# La console renvoie du texte -> SQLAlchemy attend date et heure
def convertir_date_heure(date_heure_saisie):
    try:
        return datetime.strptime(
            date_heure_saisie.strip(),
            "%d/%m/%Y %H:%M",
        )
    except ValueError:
        raise ValueError("La date et l'heure doivent être au format JJ/MM/AAAA HH:MM.")


# Le nb de participants arrive en texte donc modif
def convertir_participants(nombre_participants):
    try:
        return int(nombre_participants.strip())
    except ValueError:
        raise ValueError("Le nombre de participants doit être un nombre entier.")


# ================================ #
# Recherche des évènements
# ================================ #


# Listing évènements
def liste_evenements(session):
    requete = select(Evenement).order_by(Evenement.id)
    return session.execute(requete).scalars().all()


def recherche_evenement(session, evenement_id):
    # L'ID arrive de la console sous forme de texte -> int
    try:
        evenement_id = int(evenement_id)
    except ValueError:
        raise ValueError("L'ID de l'évènement doit être un nombre entier.")

    evenement = session.get(Evenement, evenement_id)

    if evenement is None:
        raise ValueError("Aucun évènement ne correspond à cet ID.")

    return evenement


# ================================ #
# Affectation des évènements
# ================================ #


# Évènements créés par un Commercial pas encore affectés au Support
def evenements_non_affectes_support(session):
    requete = (
        select(Evenement).where(Evenement.support_id.is_(None)).order_by(Evenement.id)
    )
    return session.execute(requete).scalars().all()


# Évènements affectés au collaborateur Support sélectionné
def evenements_affectes_support(session, support):
    requete = (
        select(Evenement)
        .where(Evenement.support_id == support.numero_employe)
        .order_by(Evenement.id)
    )
    return session.execute(requete).scalars().all()


# ================================ #
# Création d'un évènement
# ================================ #


def creation_evenement(
    session,
    contrat,
    nom,
    date_debut,
    date_fin,
    lieu,
    nombre_participants,
    notes,
):
    # Nettoyage des infos
    nom = nom.strip()
    lieu = lieu.strip()
    notes = notes.strip()

    # Données obligatoires
    if (
        not nom
        or not date_debut
        or not date_fin
        or not lieu
        or not nombre_participants
        or not notes
    ):
        raise ValueError("Toutes les informations de l'évènement sont obligatoires.")

    # Création possible si contrat signé
    if not contrat.signature:
        raise ValueError("Le contrat doit être signé avant de créer un évènement.")

    # Un contrat == un seul évènement
    if contrat.evenement is not None:
        raise ValueError("Un évènement existe déjà pour ce contrat.")

    date_debut = convertir_date_heure(date_debut)
    date_fin = convertir_date_heure(date_fin)
    nombre_participants = convertir_participants(nombre_participants)

    nouvel_evenement = Evenement(
        nom=nom,
        date_debut=date_debut,
        date_fin=date_fin,
        lieu=lieu,
        nombre_participants=nombre_participants,
        notes=notes,
        contrat=contrat,
    )

    session.add(nouvel_evenement)

    return nouvel_evenement


# ================================ #
# Affectation d'un Support
# ================================ #


def affecter_support(evenement, support):
    # Un seul collaborateur support peut-être affecté
    if support.departement.nom != "Support":
        raise ValueError(
            "Le collaborateur sélectionné n'appartient pas au Département Support."
        )

    # Non utilisation d'un même évènement
    if evenement.support is not None:
        raise ValueError(
            "Cet évènement est déjà affecté à un membre du Département Support."
        )

    evenement.support = support

    return evenement


# ================================ #
# Modification d'un évènement
# ================================ #


# Infos d'un évènement
def modification_evenement(
    evenement,
    nom,
    date_debut,
    date_fin,
    lieu,
    nombre_participants,
    notes,
):
    # Une saisie vide conserve la valeur actuelle
    if nom:
        evenement.nom = nom.strip()
    if date_debut:
        evenement.date_debut = convertir_date_heure(date_debut)
    if date_fin:
        evenement.date_fin = convertir_date_heure(date_fin)
    if lieu:
        evenement.lieu = lieu.strip()
    if nombre_participants:
        evenement.nombre_participants = convertir_participants(nombre_participants)
    if notes:
        evenement.notes = notes.strip()

    return evenement
