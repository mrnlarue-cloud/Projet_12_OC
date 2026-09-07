from sqlalchemy import text

from epic_events.controllers.clients import (
    consulter_clients,
    creer_client,
    modifier_client,
)
from epic_events.controllers.collaborateurs import (
    consulter_collaborateurs,
    creer_collaborateur,
    modifier_collaborateur,
    supprimer_collaborateur,
)
from epic_events.controllers.contrats import (
    consulter_contrats,
    consulter_contrats_non_signes,
    consulter_contrats_non_soldes,
    creer_contrat,
    modifier_contrat,
)
from epic_events.controllers.evenements import (
    affecter_support_evenement,
    consulter_evenements,
    consulter_evenements_non_affectes,
    consulter_mes_evenements_support,
    creer_evenement,
    modifier_evenement,
)
from epic_events.database import engine

# ================================ #
# Vérification de la connexion
# ================================ #


def verifier_connexion():
    # Vérifie que PostgreSQL répond avant de lancer l'app
    with engine.connect() as connexion:
        connexion.execute(text("SELECT 1"))

    print("Connexion à PostgreSQL réussie.")


# ================================ #
# Menu Collaborateurs
# ================================ #


def menu_collaborateurs():
    menu_actif = True

    while menu_actif:
        print(
            "\n===== COLLABORATEURS ====="
            "\n"
            "\n1. Consulter les collaborateurs"
            "\n2. Créer un collaborateur"
            "\n3. Modifier un collaborateur"
            "\n4. Supprimer un collaborateur"
            "\n"
            "\n0. Retour au menu principal"
        )

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            consulter_collaborateurs()
        elif choix == "2":
            creer_collaborateur()
        elif choix == "3":
            modifier_collaborateur()
        elif choix == "4":
            supprimer_collaborateur()
        elif choix == "0":
            menu_actif = False
        else:
            print("Choix invalide.")


# ================================ #
# Menu Clients
# ================================ #


def menu_clients():
    menu_actif = True

    while menu_actif:
        print(
            "\n===== CLIENTS ====="
            "\n"
            "\n1. Consulter les clients"
            "\n2. Créer un client"
            "\n3. Modifier un client"
            "\n"
            "\n0. Retour au menu principal"
        )

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            consulter_clients()
        elif choix == "2":
            creer_client()
        elif choix == "3":
            modifier_client()
        elif choix == "0":
            menu_actif = False
        else:
            print("Choix invalide.")


# ================================ #
# Menu Contrats
# ================================ #


def menu_contrats():
    menu_actif = True

    while menu_actif:
        print(
            "\n===== CONTRATS ====="
            "\n"
            "\n1. Consulter les contrats"
            "\n2. Créer un contrat"
            "\n3. Modifier un contrat"
            "\n4. Afficher les contrats non signés"
            "\n5. Afficher les contrats non soldés"
            "\n"
            "\n0. Retour au menu principal"
        )

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            consulter_contrats()
        elif choix == "2":
            creer_contrat()
        elif choix == "3":
            modifier_contrat()
        elif choix == "4":
            consulter_contrats_non_signes()
        elif choix == "5":
            consulter_contrats_non_soldes()
        elif choix == "0":
            menu_actif = False
        else:
            print("Choix invalide.")


# ================================ #
# Menu Évènements
# ================================ #


def menu_evenements():
    menu_actif = True

    while menu_actif:
        print(
            "\n===== ÉVÈNEMENTS ====="
            "\n"
            "\n1. Consulter les évènements"
            "\n2. Créer un évènement"
            "\n3. Afficher les évènements sans Support"
            "\n4. Affecter un Support à un évènement"
            "\n5. Afficher mes évènements Support"
            "\n6. Modifier un évènement"
            "\n"
            "\n0. Retour au menu principal"
        )

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            consulter_evenements()
        elif choix == "2":
            creer_evenement()
        elif choix == "3":
            consulter_evenements_non_affectes()
        elif choix == "4":
            affecter_support_evenement()
        elif choix == "5":
            consulter_mes_evenements_support()
        elif choix == "6":
            modifier_evenement()
        elif choix == "0":
            menu_actif = False
        else:
            print("Choix invalide.")


# ================================ #
# Menu principal
# ================================ #


def afficher_menu_principal():
    print(
        "\n===== EPIC EVENTS CRM ====="
        "\n"
        "\n1. Collaborateurs"
        "\n2. Clients"
        "\n3. Contrats"
        "\n4. Évènements"
        "\n"
        "\n0. Quitter"
    )

    return input("\nVotre choix : ").strip()


# ================================ #
# Lancement de l'application
# ================================ #


def lancer_application():
    # Vérifie la connexion à la DB avant d'afficher le menu
    verifier_connexion()

    application_active = True

    # Le menu reste actif jusqu'au choix de quitter
    while application_active:
        choix = afficher_menu_principal()

        if choix == "1":
            menu_collaborateurs()
        elif choix == "2":
            menu_clients()
        elif choix == "3":
            menu_contrats()
        elif choix == "4":
            menu_evenements()
        elif choix == "0":
            print("Fermeture de Epic Events CRM.")
            application_active = False
        else:
            print("Choix invalide.")


# ================================ #
# Point d'entrée du programme
# ================================ #


if __name__ == "__main__":
    # Lance l'application uniquement si main.py est exécuté directement
    lancer_application()
