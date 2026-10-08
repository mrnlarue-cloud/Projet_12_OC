# ================================ #
# Imports
# ================================ #

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from epic_events.database import Base
from epic_events.models.clients import Client
from epic_events.models.contrats import Contrat
from epic_events.models.departement import Departement
from epic_events.models.evenements import Evenement
from epic_events.security.chiffrement import TexteChiffre
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

    # Nom chiffré et email utilisé pour l'authentification
    nom: Mapped[str] = mapped_column(TexteChiffre(), nullable=False)
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


# ================================ #
# Recherche des collaborateurs
# ================================ #


def liste_collaborateurs(session):
    requete = select(Collaborateur).order_by(Collaborateur.numero_employe)
    return session.execute(requete).scalars().all()


def recherche_collaborateur(session, numero_employe):
    try:
        numero_employe = int(numero_employe)
    except (TypeError, ValueError):
        raise ValueError("Votre numéro employé doit être un nombre entier.")

    collaborateur = session.get(Collaborateur, numero_employe)

    if collaborateur is None:
        raise ValueError("Aucun collaborateur ne correspond à ce numéro employé.")

    return collaborateur


# ================================ #
# Création courante d'un collaborateur
# ================================ #


def creation_collaborateur(
    session,
    nom,
    email,
    mdp,
    confirmation_mdp,
    nom_departement,
):
    # Nettoyage des infos de texte
    nom = nom.strip()
    email = email.strip()
    nom_departement = nom_departement.strip()

    # Informations obligatoires
    if not nom or not email or not mdp:
        raise ValueError("Le nom, l'email et le mot de passe sont obligatoires.")

    if mdp != confirmation_mdp:
        raise ValueError("Les mots de passe ne correspondent pas.")

    # Refus si email déjà utilisé
    requete = select(Collaborateur).where(Collaborateur.email == email)
    collaborateur_existant = session.execute(requete).scalar_one_or_none()

    if collaborateur_existant is not None:
        raise ValueError("Cet email est déjà utilisé.")

    # Vérification du département demandé
    if nom_departement not in ("Gestion", "Commercial", "Support"):
        raise ValueError("Choisissez un département : Gestion, Commercial ou Support.")

    requete = select(Departement).where(Departement.nom == nom_departement)
    departement = session.execute(requete).scalar_one_or_none()

    if departement is None:
        raise ValueError("Ce département n'existe pas.")

    # Ajout du nouveau collaborateur
    nouveau_collaborateur = Collaborateur(
        nom=nom,
        email=email,
        mot_de_passe_hash=hash_mdp(mdp),
        departement=departement,
    )
    session.add(nouveau_collaborateur)

    return nouveau_collaborateur


# ================================ #
# Modification d'un collaborateur
# ================================ #


def modification_collaborateur(
    session,
    collaborateur,
    nom,
    email,
    mdp,
    confirmation_mdp,
    nom_departement,
):
    # Vérification de l'email si renseigné
    if email:
        email = email.strip()
        requete = select(Collaborateur).where(
            Collaborateur.email == email,
            Collaborateur.numero_employe != collaborateur.numero_employe,
        )
        collaborateur_existant = session.execute(requete).scalar_one_or_none()

        if collaborateur_existant is not None:
            raise ValueError("Cet email est déjà utilisé.")

        collaborateur.email = email

    # Modif nom si renseigné
    if nom:
        collaborateur.nom = nom.strip()

    # Remplace le MDP uniquement si les deux saisies correspondent
    if mdp != confirmation_mdp:
        raise ValueError("Les mots de passe ne correspondent pas.")

    if mdp:
        collaborateur.mot_de_passe_hash = hash_mdp(mdp)

    # Modif département si renseigné
    if nom_departement:
        nom_departement = nom_departement.strip()

        if nom_departement not in ("Gestion", "Commercial", "Support"):
            raise ValueError(
                "Choisissez un département : Gestion, Commercial ou Support."
            )

        requete = select(Departement).where(Departement.nom == nom_departement)
        departement = session.execute(requete).scalar_one_or_none()

        if departement is None:
            raise ValueError("Ce département n'existe pas.")

        changement_departement = departement.id != collaborateur.departement_id
        donnees_associees = (
            collaborateur.clients or collaborateur.contrats or collaborateur.evenements
        )

        if changement_departement and donnees_associees:
            # Impossible car des clients, contrats ou événements
            # sont encore associés au collaborateur
            raise ValueError("Ce collaborateur possède encore des données associées.")

        collaborateur.departement = departement

    return collaborateur


# ================================ #
# Suppression d'un collaborateur
# ================================ #


def suppression_collaborateur(session, collaborateur):
    # Impossible car des clients, contrats ou événements
    # sont encore associés au collaborateur
    if collaborateur.clients or collaborateur.contrats or collaborateur.evenements:
        raise ValueError("Ce collaborateur possède encore des données associées.")

    session.delete(collaborateur)
