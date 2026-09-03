from epic_events.database import SessionLocale
from epic_events.models.clients import (
    creation_client,
    liste_clients,
    modification_client,
    recherche_client,
)
from epic_events.security.authentification import authentification_collaborateurs
from epic_events.security.permissions import (
    verifier_authentification,
    verifier_commercial,
    verifier_modif_client,
)
from epic_events.views.clients import (
    afficher_client,
    afficher_clients,
    afficher_message,
    saisir_client_id,
    saisir_infos_client,
    saisir_modifications_client,
)
from epic_events.views.collaborateurs import saisir_identifiants

# ================================ #
# Contrôleur clients : Consultation
# ================================ #


def consulter_clients():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        # Identifie l'utilisateur avant tout accès clients
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        # La lecture est autorisée aux trois départements
        verifier_authentification(utilisateur_connecte)

        clients = liste_clients(session)
        afficher_clients(clients)

    except (ValueError, PermissionError) as erreur:
        afficher_message(str(erreur))

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


# ================================ #
# Contrôleur clients : Création
# ================================ #


def creer_client():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        # La création est réservée au département Commercial
        verifier_commercial(utilisateur_connecte)

        (
            nom_complet,
            email_client,
            telephone,
            entreprise,
            date_creation_contact,
            date_dernier_echange,
        ) = saisir_infos_client()

        # L'utilisateur authentifié devient le responsable du client
        nouveau_client = creation_client(
            session,
            utilisateur_connecte,
            nom_complet,
            email_client,
            telephone,
            entreprise,
            date_creation_contact,
            date_dernier_echange,
        )

        session.commit()

        # Conserve l'ID avant la fermeture de la session
        client_id = nouveau_client.id

    except (ValueError, PermissionError) as erreur:
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message(f"Le client {client_id} a été créé.")


# ================================ #
# Contrôleur clients : Modification
# ================================ #


def modifier_client():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        verifier_authentification(utilisateur_connecte)

        client_id = saisir_client_id()
        client = recherche_client(
            session,
            client_id,
        )

        # La permission dépend du propriétaire du client sélectionné
        verifier_modif_client(
            utilisateur_connecte,
            client,
        )

        # Affiche les valeurs actuelles avant les changements
        afficher_client(client)

        (
            nom_complet,
            email_client,
            telephone,
            entreprise,
            date_creation_contact,
            date_dernier_echange,
        ) = saisir_modifications_client()

        modification_client(
            client,
            nom_complet,
            email_client,
            telephone,
            entreprise,
            date_creation_contact,
            date_dernier_echange,
        )

        session.commit()

    except (ValueError, PermissionError) as erreur:
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message("Le client a été modifié.")