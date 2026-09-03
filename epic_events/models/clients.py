from datetime import date, datetime

from sqlalchemy import Date, ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base

# ================================ #
# Modèle métier de Client
# ================================ #


class Client(Base):
    __tablename__ = "clients"

    # ================================ #
    # Champs obligatoires
    # ================================ #

    id: Mapped[int] = mapped_column(primary_key=True)

    # Infos client
    nom_complet: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    telephone: Mapped[str] = mapped_column(String, nullable=False)
    entreprise: Mapped[str] = mapped_column(String, nullable=False)
    date_creation_contact: Mapped[date] = mapped_column(Date, nullable=False)
    date_dernier_echange: Mapped[date] = mapped_column(Date, nullable=False)

    # Commercial responsable
    commercial_id: Mapped[int] = mapped_column(
        ForeignKey("collaborateurs.numero_employe"), nullable=False
    )

    # ================================ #
    # Relations
    # ================================ #

    commercial = relationship("Collaborateur", back_populates="clients")
    contrats = relationship("Contrat", back_populates="client")


# ================================ #
# Conversion des dates
# ================================ #


# La console renvoie du texte, mais SQLAlchemy attend une date Python
def convertir_date(date_saisie):
    try:
        return datetime.strptime(date_saisie.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("La date doit être au format JJ/MM/AAAA.")


# ================================ #
# Recherche des clients
# ================================ #


def liste_clients(session):
    # Tri par ID
    requete = select(Client).order_by(Client.id)
    return session.execute(requete).scalars().all()


def recherche_client(session, client_id):
    # L'ID -> console sous forme de texte
    try:
        client_id = int(client_id)
    except ValueError:
        raise ValueError("L'ID du client doit être un nombre entier.")

    client = session.get(Client, client_id)

    if client is None:
        raise ValueError("Aucun client ne correspond à cet ID.")

    return client


# ================================ #
# Création d'un client
# ================================ #


def creation_client(
    session,
    commercial,
    nom_complet,
    email,
    telephone,
    entreprise,
    date_creation_contact,
    date_dernier_echange,
):
    # Nettoyage données
    nom_complet = nom_complet.strip()
    email = email.strip()
    telephone = telephone.strip()
    entreprise = entreprise.strip()

    if (
        not nom_complet
        or not email
        or not telephone
        or not entreprise
        or not date_creation_contact
        or not date_dernier_echange
    ):
        raise ValueError("Toutes les informations du client sont obligatoires.")

    date_creation_contact = convertir_date(date_creation_contact)
    date_dernier_echange = convertir_date(date_dernier_echange)

    # Le responsable est toujours le Commercial connecté
    nouveau_client = Client(
        nom_complet=nom_complet,
        email=email,
        telephone=telephone,
        entreprise=entreprise,
        date_creation_contact=date_creation_contact,
        date_dernier_echange=date_dernier_echange,
        commercial=commercial,
    )

    session.add(nouveau_client)

    return nouveau_client


# ================================ #
# Modification d'un client
# ================================ #


def modification_client(
    client,
    nom_complet,
    email,
    telephone,
    entreprise,
    date_creation_contact,
    date_dernier_echange,
):
    nom_complet = nom_complet.strip()
    email = email.strip()
    telephone = telephone.strip()
    entreprise = entreprise.strip()

    # Lorsque rien n'est saisi, on conserve la valeur existante
    if nom_complet:
        client.nom_complet = nom_complet
    if email:
        client.email = email
    if telephone:
        client.telephone = telephone
    if entreprise:
        client.entreprise = entreprise
    if date_creation_contact:
        client.date_creation_contact = convertir_date(date_creation_contact)
    if date_dernier_echange:
        client.date_dernier_echange = convertir_date(date_dernier_echange)

    return client
