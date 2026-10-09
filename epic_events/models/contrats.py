# ================================ #
# Imports
# ================================ #

from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from sqlalchemy import Boolean, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base
from epic_events.security.chiffrement import DateChiffree, MontantChiffre

# ================================ #
# Modèle métier de Contrat
# ================================ #


class Contrat(Base):
    __tablename__ = "contrats"

    # ================================ #
    # Champs obligatoires
    # ================================ #

    id: Mapped[int] = mapped_column(primary_key=True)

    # Infos du contrat
    montant_total: Mapped[Decimal] = mapped_column(MontantChiffre(), nullable=False)
    montant_restant: Mapped[Decimal] = mapped_column(MontantChiffre(), nullable=False)
    date_creation: Mapped[date] = mapped_column(DateChiffree(), nullable=False)
    signature: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Client et Commercial associés
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    commercial_id: Mapped[int] = mapped_column(
        ForeignKey("collaborateurs.numero_employe"), nullable=False
    )

    # ================================ #
    # Relations
    # ================================ #

    client = relationship("Client", back_populates="contrats")
    commercial = relationship("Collaborateur", back_populates="contrats")
    evenement = relationship("Evenement", back_populates="contrat", uselist=False)


# ================================ #
# Conversion des saisies
# ================================ #


# Conversion du montant saisi en Decimal
def convertir_montant(montant_saisi):
    try:
        return Decimal(montant_saisi.strip().replace(",", "."))
    except InvalidOperation:
        raise ValueError("Le montant doit être un nombre.")


# La console renvoie du texte, mais SQLAlchemy attend une date Python
def convertir_date(date_saisie):
    try:
        return datetime.strptime(date_saisie.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("La date doit être au format JJ/MM/AAAA.")


# La réponse OUI ou NON devient un booléen
def convertir_signature(signature_saisie):
    signature_saisie = signature_saisie.strip().upper()

    if signature_saisie == "OUI":
        return True
    if signature_saisie == "NON":
        return False

    raise ValueError("La signature doit être indiquée par OUI ou NON.")


# ================================ #
# Recherche des contrats
# ================================ #


def liste_contrats(session):
    requete = select(Contrat).order_by(Contrat.id)
    return session.execute(requete).scalars().all()


def recherche_contrat(session, contrat_id):
    # L'ID arrive de la console sous forme de texte -> int
    try:
        contrat_id = int(contrat_id)
    except ValueError:
        raise ValueError("L'ID du contrat doit être un nombre entier.")

    contrat = session.get(Contrat, contrat_id)

    if contrat is None:
        raise ValueError("Aucun contrat ne correspond à cet ID.")

    return contrat


# ================================ #
# Filtres des contrats
# ================================ #


def contrats_non_signes(session):
    requete = select(Contrat).where(Contrat.signature.is_(False)).order_by(Contrat.id)
    return session.execute(requete).scalars().all()


def contrats_non_soldes(session):
    # Filtrage des montants après déchiffrement
    contrats = liste_contrats(session)
    return [contrat for contrat in contrats if contrat.montant_restant > 0]


# ================================ #
# Création d'un contrat
# ================================ #


def creation_contrat(
    session,
    client,
    montant_total,
    montant_restant,
    date_creation,
    signature,
):
    if not montant_total or not montant_restant or not date_creation or not signature:
        raise ValueError("Toutes les informations du contrat sont obligatoires.")

    montant_total = convertir_montant(montant_total)
    montant_restant = convertir_montant(montant_restant)
    date_creation = convertir_date(date_creation)
    signature = convertir_signature(signature)

    # Le Commercial du contrat est celui du client
    nouveau_contrat = Contrat(
        montant_total=montant_total,
        montant_restant=montant_restant,
        date_creation=date_creation,
        signature=signature,
        client=client,
        commercial=client.commercial,
    )

    session.add(nouveau_contrat)

    return nouveau_contrat


# ================================ #
# Modification d'un contrat
# ================================ #


def modification_contrat(
    contrat,
    montant_total,
    montant_restant,
    date_creation,
    signature,
):
    # Une saisie vide conserve la valeur actuelle
    if montant_total:
        contrat.montant_total = convertir_montant(montant_total)
    if montant_restant:
        contrat.montant_restant = convertir_montant(montant_restant)
    if date_creation:
        contrat.date_creation = convertir_date(date_creation)
    if signature:
        contrat.signature = convertir_signature(signature)

    return contrat
