from unittest.mock import Mock

from epic_events.security.authentification import authentification_collaborateurs
from epic_events.security.mot_de_passe import hash_mdp

# ================================
# Tests unitaires d'authentification
# ================================


def test_authentification_email_inconnu():
    # Simule un résultat de recherche sans collaborateur et sans DB
    resultat = Mock()
    resultat.scalar_one_or_none.return_value = None

    # Simule une session
    session = Mock()
    session.execute.return_value = resultat

    # Tentative de connexion d'un utilisateur non connu
    collaborateur = authentification_collaborateurs(
        session, "inconnu@test.com", "mdp_test"
    )

    assert collaborateur is None


def test_authentification_mdp_incorrect():
    # Simule un bon collaborateur avec MDP & hash
    collaborateur = Mock()
    collaborateur.mot_de_passe_hash = hash_mdp("bon_mdp_test")

    # Collaborateur existant
    resultat = Mock()
    resultat.scalar_one_or_none.return_value = collaborateur

    # Simulation de la session
    session = Mock()
    session.execute.return_value = resultat

    # Tentative de co. mauvais MDP
    connexion = authentification_collaborateurs(
        session, "connu@test.com", "mauvais_mdp_test"
    )

    assert connexion is None


def test_authentification_identifiants_corrects():
    # Simule un bon collaborateur avec MDP & hash
    collaborateur = Mock()
    collaborateur.mot_de_passe_hash = hash_mdp("bon_mdp_test")

    # Collaborateur ok
    resultat = Mock()
    resultat.scalar_one_or_none.return_value = collaborateur

    session = Mock()
    session.execute.return_value = resultat

    # Tentative de co. bon MDP
    connexion = authentification_collaborateurs(
        session, "connu@test.com", "bon_mdp_test"
    )

    assert connexion is collaborateur
