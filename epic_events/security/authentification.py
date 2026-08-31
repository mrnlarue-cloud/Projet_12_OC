from sqlalchemy import select

from epic_events.models.collaborateur import Collaborateur
from epic_events.security.mot_de_passe import verification_mdp

# ================================
# Authentification des collaborateurs
# ================================


def authentification_collaborateurs(session, email, mdp):
    """Recherche et vérifie les identifiants du collaborateur.

    select : prépare une recherche sur le modèle Collaborateur
    where : filtre sur l'e-mail reçu
    session.execute : exécute la recherche dans la DB
    scalar_one_or_none : extrait un objet Collaborateur ou None si absent
    """

    requete = select(Collaborateur).where(Collaborateur.email == email)
    collaborateur = session.execute(requete).scalar_one_or_none()

    # Refus email inconnu
    if collaborateur is None:
        return None

    # Refus mauvais MDP
    if not verification_mdp(collaborateur.mot_de_passe_hash, mdp):
        return None

    # Sinon retourne le collaborateur authentifié
    return collaborateur
