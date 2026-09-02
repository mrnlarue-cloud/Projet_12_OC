from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from epic_events.database import Base
from epic_events.models.clients import Client
from epic_events.models.collaborateur import (
    Collaborateur,
    creation_collaborateur,
    creation_premier_gestionnaire,
    liste_collaborateurs,
    modification_collaborateur,
    recherche_collaborateur,
    suppression_collaborateur,
)

# ================================ #
# Test d'intégration du modèle Collaborateur
# ================================ #


def test_parcours_complet_collaborateur():
    # Création de la DB temporaire
    moteur_test = create_engine("sqlite:///:memory:")
    SessionTest = sessionmaker(bind=moteur_test)
    Base.metadata.create_all(bind=moteur_test)

    # Ouverture d'une seule session
    session = SessionTest()

    try:
        # ================================ #
        # Création du premier compte Gestion
        # ================================ #

        gestionnaire = creation_premier_gestionnaire(
            session,
            "Gestion Test",
            "gestion.integration@exemple.test",
            "Demonstration-Gestion-Test!",
            "Demonstration-Gestion-Test!",
        )

        session.commit()

        # Vérifie le département du premier compte
        assert gestionnaire.departement.nom == "Gestion"

        # ================================ #
        # Création d'un Commercial
        # ================================ #

        commercial = creation_collaborateur(
            session,
            "Commercial Test",
            "commercial.integration@exemple.test",
            "Demonstration-Commercial-Test!",
            "Demonstration-Commercial-Test!",
            "Commercial",
        )

        session.commit()

        # Conserve le numéro créé par la DB
        numero_employe = commercial.numero_employe

        # Vérifie les données enregistrées
        resultat_creation = (
            commercial.nom,
            commercial.email,
            commercial.departement.nom,
        )

        assert resultat_creation == (
            "Commercial Test",
            "commercial.integration@exemple.test",
            "Commercial",
        )

        # ================================ #
        # Consultation des collaborateurs
        # ================================ #

        collaborateurs = liste_collaborateurs(session)

        emails_collaborateurs = [
            collaborateur.email for collaborateur in collaborateurs
        ]

        assert emails_collaborateurs == [
            "gestion.integration@exemple.test",
            "commercial.integration@exemple.test",
        ]

        # ================================ #
        # Recherche du Commercial
        # ================================ #

        commercial_trouve = recherche_collaborateur(
            session,
            numero_employe,
        )

        assert commercial_trouve.email == ("commercial.integration@exemple.test")

        # ================================ #
        # Modification du Commercial
        # ================================ #

        modification_collaborateur(
            session,
            commercial,
            "Commercial Modifié",
            "commercial.modifie@exemple.test",
            "",
            "",
            "",
        )

        session.commit()

        # Vérifie uniquement les données modifiées
        resultat_modification = (
            commercial.nom,
            commercial.email,
        )

        assert resultat_modification == (
            "Commercial Modifié",
            "commercial.modifie@exemple.test",
        )

        # ================================ #
        # Ajout d'un client associé
        # ================================ #

        client = Client(
            nom_complet="Client Test",
            email="client.integration@exemple.test",
            telephone="0102030405",
            entreprise="Entreprise Test",
            date_creation_contact=date(2026, 1, 1),
            date_dernier_echange=date(2026, 1, 1),
            commercial=commercial,
        )

        session.add(client)
        session.commit()

        # ================================ #
        # Refus du changement de département
        # ================================ #

        with pytest.raises(ValueError) as erreur_departement:
            modification_collaborateur(
                session,
                commercial,
                "",
                "",
                "",
                "",
                "Support",
            )

        assert str(erreur_departement.value) == (
            "Ce collaborateur possède encore des données associées."
        )

        # ================================ #
        # Refus de la suppression
        # ================================ #

        with pytest.raises(ValueError) as erreur_suppression:
            suppression_collaborateur(
                session,
                commercial,
            )

        assert str(erreur_suppression.value) == (
            "Ce collaborateur possède encore des données associées."
        )

        # ================================ #
        # Retrait du client associé
        # ================================ #

        session.delete(client)
        session.commit()

        # Ferme puis recharge les données actuelles
        session.close()
        session = SessionTest()

        commercial = recherche_collaborateur(
            session,
            numero_employe,
        )

        # ================================ #
        # Suppression du Commercial
        # ================================ #

        suppression_collaborateur(
            session,
            commercial,
        )

        session.commit()

        # Vérifie sa disparition dans la DB
        commercial_supprime = session.get(
            Collaborateur,
            numero_employe,
        )

        assert commercial_supprime is None

    finally:
        # Ferme la session et détruit la DB
        session.close()
        moteur_test.dispose()
