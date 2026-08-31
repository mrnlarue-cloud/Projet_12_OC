# String = texte en BDD, ForeignKey = ID lié à une autre table
from sqlalchemy import ForeignKey, String, select

# Mapped = type Python, mapped_column = colonne SQL
# relationship = lien entre les objets Python
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base
from epic_events.models.clients import Client
from epic_events.models.contrats import Contrat
from epic_events.models.departement import Departement
from epic_events.models.evenements import Evenement
from epic_events.security.mot_de_passe import hash_mdp

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
    # Relations entre modèles
    # ================================ #

    # Accès au département du collaborateur
    departement = relationship(Departement, back_populates="collaborateurs")

    # Accès aux clients dont le collaborateur est le commercial
    clients = relationship(Client, back_populates="commercial")

    # Accès aux contrats dont le collaborateur est le commercial
    contrats = relationship(Contrat, back_populates="commercial")

    # Accès aux événements dont le collaborateur est le support
    evenements = relationship(Evenement, back_populates="support")


# ================================ #
# Création du premier compte Gestion
# ================================ #


def creation_premier_gestionnaire(session, nom, email, mdp, confirmation_mdp):
    # Recherche un collaborateur déjà existant (max 1)
    requete = select(Collaborateur).limit(1)
    collaborateur = session.execute(requete).scalar_one_or_none()

    if collaborateur is not None:
        raise ValueError("Le collaborateur existe déjà : Création non autorisée.")

    # Vérifie les informations obligatoires
    if not nom or not email or not mdp:
        raise ValueError("Le nom, l'email et le mot de passe sont obligatoires.")

    if mdp != confirmation_mdp:
        raise ValueError("Les mots de passe ne correspondent pas.")

    # Récupère ou prépare les trois départements
    for nom_departement in ("Gestion", "Commercial", "Support"):
        requete = select(Departement).where(Departement.nom == nom_departement)
        departement = session.execute(requete).scalar_one_or_none()

        if departement is None:
            departement = Departement(nom=nom_departement)
            session.add(departement)

        # Conserve le département du premier compte
        if nom_departement == "Gestion":
            gestion = departement

    # Transforme le MDP saisi en hash
    mdp_hash = hash_mdp(mdp)

    # Prépare le collaborateur rattaché à Gestion
    collaborateur = Collaborateur(
        nom=nom,
        email=email,
        mot_de_passe_hash=mdp_hash,
        departement=gestion,
    )
    session.add(collaborateur)

    return collaborateur
