import pytest

from epic_events.models.clients import Client
from epic_events.models.collaborateur import Collaborateur
from epic_events.models.departement import Departement
from epic_events.security.permissions import (
    verifier_authentification,
    verifier_commercial,
    verifier_gestion,
    verifier_modif_client,
)

# ================================ #
# Test des permissions
# ================================ #


def test_permissions_collaborateurs():
    # Création des départements fictifs
    gestion = Departement(nom="Gestion")
    commercial = Departement(nom="Commercial")

    # Création des collaborateurs fictifs
    gestionnaire = Collaborateur(
        numero_employe=1,
        departement=gestion,
    )
    commercial_responsable = Collaborateur(
        numero_employe=2,
        departement=commercial,
    )
    autre_commercial = Collaborateur(
        numero_employe=3,
        departement=commercial,
    )

    # Création d'un client fictif
    client = Client(
        commercial_id=2,
    )

    # ================================ #
    # Permissions autorisées
    # ================================ #

    # Autorise un utilisateur authentifié
    verifier_authentification(gestionnaire)

    # Autorise le département Gestion
    verifier_gestion(gestionnaire)

    # Autorise le département Commercial
    verifier_commercial(commercial_responsable)

    # Autorise le responsable de son propre client
    verifier_modif_client(
        commercial_responsable,
        client,
    )

    # ================================ #
    # Refus d'authentification
    # ================================ #

    with pytest.raises(PermissionError) as erreur_authentification:
        verifier_authentification(None)

    assert str(erreur_authentification.value) == (
        "Vous devez impérativement être connecté."
    )

    # Vérifie aussi le refus direct de Gestion
    with pytest.raises(PermissionError) as erreur_gestion_absente:
        verifier_gestion(None)

    assert str(erreur_gestion_absente.value) == (
        "Vous devez impérativement être connecté."
    )

    # ================================ #
    # Refus du département Gestion
    # ================================ #

    with pytest.raises(PermissionError) as erreur_gestion:
        verifier_gestion(commercial_responsable)

    assert str(erreur_gestion.value) == (
        "Cette action est réservée au département Gestion."
    )

    # ================================ #
    # Refus du département Commercial
    # ================================ #

    with pytest.raises(PermissionError) as erreur_commercial:
        verifier_commercial(gestionnaire)

    assert str(erreur_commercial.value) == (
        "Cette action est réservée au département Commercial."
    )

    # ================================ #
    # Refus de modification d'un client
    # ================================ #

    with pytest.raises(PermissionError) as erreur_client:
        verifier_modif_client(
            autre_commercial,
            client,
        )

    assert str(erreur_client.value) == (
        "Vous ne pouvez modifier que vos propres clients."
    )
