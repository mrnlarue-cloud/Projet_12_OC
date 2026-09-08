from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from epic_events.controllers import clients as controleur_clients
from epic_events.controllers import collaborateurs as controleur_collaborateurs
from epic_events.controllers import contrats as controleur_contrats
from epic_events.controllers import evenements as controleur_evenements
from epic_events.database import Base
from epic_events.models.clients import Client
from epic_events.models.collaborateur import Collaborateur
from epic_events.models.contrats import Contrat
from epic_events.models.departement import Departement
from epic_events.models.evenements import Evenement

# ================================ #
# Données du parcours d'intégration
# ================================ #


def infos_gestion():
    return (
        "Gestion Test",
        "gestion.test@exemple.test",
        "Gestion-Test!",
        "Gestion-Test!",
    )


def identifiants_gestion():
    return "gestion.test@exemple.test", "Gestion-Test!"


def infos_commercial():
    return (
        "Commercial Test",
        "commercial.test@exemple.test",
        "Commercial-Test!",
        "Commercial-Test!",
    )


def identifiants_commercial():
    return "commercial.test@exemple.test", "Commercial-Test!"


def infos_support():
    return (
        "Support Test",
        "support.test@exemple.test",
        "Support-Test!",
        "Support-Test!",
    )


def identifiants_support():
    return "support.test@exemple.test", "Support-Test!"


def departement_commercial():
    return "Commercial"


def departement_support():
    return "Support"


def infos_client():
    return (
        "Client Test",
        "client.test@exemple.test",
        "0102030405",
        "Entreprise Test",
        "01/09/2026",
        "08/09/2026",
    )


# ================================ #
# Test du parcours métier complet
# ================================ #


def test_parcours_integration_complet(monkeypatch, tmp_path):
    # Crée une base SQLite temporaire uniquement pour ce test
    chemin_bdd = tmp_path / "epic_events_test.db"

    # Crée le moteur SQLAlchemy relié à cette base temporaire
    moteur_test = create_engine(f"sqlite:///{chemin_bdd.as_posix()}")

    # Crée les sessions utilisées pendant le test avec ce moteur
    SessionTest = sessionmaker(bind=moteur_test)

    Base.metadata.create_all(
        bind=moteur_test,
        tables=[
            Departement.__table__,
            Collaborateur.__table__,
            Client.__table__,
            Contrat.__table__,
            Evenement.__table__,
        ],
    )

    # Tous les contrôleurs utilisent uniquement la base temporaire
    monkeypatch.setattr(
        controleur_collaborateurs,
        "SessionLocale",
        SessionTest,
    )
    monkeypatch.setattr(
        controleur_clients,
        "SessionLocale",
        SessionTest,
    )
    monkeypatch.setattr(
        controleur_contrats,
        "SessionLocale",
        SessionTest,
    )
    monkeypatch.setattr(
        controleur_evenements,
        "SessionLocale",
        SessionTest,
    )

    # ================================ #
    # Création du compte Gestion
    # ================================ #

    monkeypatch.setattr(
        controleur_collaborateurs,
        "saisir_infos_collaborateur",
        infos_gestion,
    )

    controleur_collaborateurs.creer_premier_compte_gestion()

    # ================================ #
    # Création du Commercial
    # ================================ #

    monkeypatch.setattr(
        controleur_collaborateurs,
        "saisir_identifiants",
        identifiants_gestion,
    )
    monkeypatch.setattr(
        controleur_collaborateurs,
        "saisir_infos_collaborateur",
        infos_commercial,
    )
    monkeypatch.setattr(
        controleur_collaborateurs,
        "saisir_departement",
        departement_commercial,
    )

    controleur_collaborateurs.creer_collaborateur()

    # ================================ #
    # Création du Support
    # ================================ #

    monkeypatch.setattr(
        controleur_collaborateurs,
        "saisir_infos_collaborateur",
        infos_support,
    )
    monkeypatch.setattr(
        controleur_collaborateurs,
        "saisir_departement",
        departement_support,
    )

    controleur_collaborateurs.creer_collaborateur()

    # ================================ #
    # Création du client
    # ================================ #

    monkeypatch.setattr(
        controleur_clients,
        "saisir_identifiants",
        identifiants_commercial,
    )
    monkeypatch.setattr(
        controleur_clients,
        "saisir_infos_client",
        infos_client,
    )

    controleur_clients.creer_client()

    session = SessionTest()

    client = session.execute(
        select(Client).where(Client.email == "client.test@exemple.test")
    ).scalar_one()

    client_id = client.id
    session.close()

    def infos_contrat():
        return (
            str(client_id),
            "5000",
            "2500",
            "08/09/2026",
            "OUI",
        )

    # ================================ #
    # Création du contrat signé
    # ================================ #

    monkeypatch.setattr(
        controleur_contrats,
        "saisir_identifiants",
        identifiants_gestion,
    )
    monkeypatch.setattr(
        controleur_contrats,
        "saisir_infos_contrat",
        infos_contrat,
    )

    controleur_contrats.creer_contrat()

    session = SessionTest()

    contrat = session.execute(select(Contrat)).scalar_one()
    contrat_id = contrat.id

    session.close()

    def infos_evenement():
        return (
            str(contrat_id),
            "Evenement Integration",
            "10/09/2026 14:00",
            "10/09/2026 18:00",
            "Paris",
            "5",
            "Test du parcours integration",
        )

    # ================================ #
    # Création de l'évènement
    # ================================ #

    monkeypatch.setattr(
        controleur_evenements,
        "saisir_identifiants",
        identifiants_commercial,
    )
    monkeypatch.setattr(
        controleur_evenements,
        "saisir_infos_evenement",
        infos_evenement,
    )

    controleur_evenements.creer_evenement()

    session = SessionTest()

    evenement = session.execute(select(Evenement)).scalar_one()
    evenement_id = evenement.id

    support = session.execute(
        select(Collaborateur).where(Collaborateur.email == "support.test@exemple.test")
    ).scalar_one()

    support_id = support.numero_employe

    session.close()

    def evenement_selectionne():
        return str(evenement_id)

    def support_selectionne():
        return str(support_id)

    # ================================ #
    # Affectation du Support
    # ================================ #

    monkeypatch.setattr(
        controleur_evenements,
        "saisir_identifiants",
        identifiants_gestion,
    )
    monkeypatch.setattr(
        controleur_evenements,
        "saisir_evenement_id",
        evenement_selectionne,
    )
    monkeypatch.setattr(
        controleur_evenements,
        "saisir_numero_support",
        support_selectionne,
    )

    controleur_evenements.affecter_support_evenement()

    # ================================ #
    # Modification par le Support
    # ================================ #

    def modifications_evenement():
        return (
            "",
            "",
            "",
            "Paris - Salle principale",
            "50",
            "Evenement modifie par le Support",
        )

    monkeypatch.setattr(
        controleur_evenements,
        "saisir_identifiants",
        identifiants_support,
    )
    monkeypatch.setattr(
        controleur_evenements,
        "saisir_evenement_id",
        evenement_selectionne,
    )
    monkeypatch.setattr(
        controleur_evenements,
        "saisir_modifications_evenement",
        modifications_evenement,
    )

    controleur_evenements.modifier_evenement()

    # ================================ #
    # Vérification finale en base
    # ================================ #

    session = SessionTest()

    client = session.execute(select(Client)).scalar_one()
    contrat = session.execute(select(Contrat)).scalar_one()
    evenement = session.execute(select(Evenement)).scalar_one()

    collaborateurs = session.execute(select(Collaborateur)).scalars().all()

    assert len(collaborateurs) == 3

    assert client.commercial.email == "commercial.test@exemple.test"

    assert contrat.client_id == client.id
    assert contrat.commercial_id == client.commercial_id
    assert contrat.signature is True

    assert evenement.contrat_id == contrat.id
    assert evenement.support.email == "support.test@exemple.test"
    assert evenement.lieu == "Paris - Salle principale"
    assert evenement.nombre_participants == 50
    assert evenement.notes == "Evenement modifie par le Support"

    session.close()
    moteur_test.dispose()
