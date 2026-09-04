from epic_events.database import SessionLocale
from epic_events.models.contrats import recherche_contrat
from epic_events.models.evenements import (
    creation_evenement,
    liste_evenements,
)
from epic_events.security.authentification import authentification_collaborateurs
from epic_events.security.permissions import (
    verifier_authentification,
    verifier_creation_evenement,
)
from epic_events.views.collaborateurs import saisir_identifiants
from epic_events.views.evenements import (
    afficher_evenements,
    afficher_message,
    saisir_infos_evenement,
)

# ================================ #
# Contrôleur évènements : Consultation
# ================================ #


def consulter_evenements():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        # Lecture autorisée aux trois départements
        verifier_authentification(utilisateur_connecte)

        evenements = liste_evenements(session)
        afficher_evenements(evenements)

    except (ValueError, PermissionError) as erreur:
        afficher_message(str(erreur))

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


# ================================ #
# Contrôleur évènements : Création
# ================================ #


def creer_evenement():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        (
            contrat_id,
            nom,
            date_debut,
            date_fin,
            lieu,
            nombre_participants,
            notes,
        ) = saisir_infos_evenement()

        contrat = recherche_contrat(
            session,
            contrat_id,
        )

        # Vérifie que le Commercial est responsable du contrat
        verifier_creation_evenement(
            utilisateur_connecte,
            contrat,
        )

        nouvel_evenement = creation_evenement(
            session,
            contrat,
            nom,
            date_debut,
            date_fin,
            lieu,
            nombre_participants,
            notes,
        )

        session.commit()

        # Conserve l'ID avant la fermeture de la session
        evenement_id = nouvel_evenement.id

    except (ValueError, PermissionError) as erreur:
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message(f"L'évènement {evenement_id} a été créé.")
