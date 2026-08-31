from unittest.mock import Mock

from epic_events.security.authentification import authentification_collaborateurs

# ================================
# Test unitaire d'authentification
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
