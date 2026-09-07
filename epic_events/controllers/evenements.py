from epic_events.database import SessionLocale
from epic_events.models.collaborateur import recherche_collaborateur
from epic_events.models.contrats import recherche_contrat
from epic_events.models.evenements import (
    affecter_support,
    creation_evenement,
    evenements_affectes_support,
    evenements_non_affectes_support,
    liste_evenements,
    modification_evenement,
    recherche_evenement,
)
from epic_events.security.authentification import authentification_collaborateurs
from epic_events.security.permissions import (
    verifier_authentification,
    verifier_creation_evenement,
    verifier_gestion,
    verifier_modif_evenement,
)
from epic_events.views.collaborateurs import saisir_identifiants
from epic_events.views.evenements import (
    afficher_evenement,
    afficher_evenements,
    afficher_message,
    saisir_evenement_id,
    saisir_infos_evenement,
    saisir_modifications_evenement,
    saisir_numero_support,
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


# ================================ #
# Contrôleur évènements : Sans Support
# ================================ #


def consulter_evenements_non_affectes():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        verifier_gestion(utilisateur_connecte)

        evenements = evenements_non_affectes_support(session)
        afficher_evenements(evenements)

    except (ValueError, PermissionError) as erreur:
        afficher_message(str(erreur))

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


# ================================ #
# Contrôleur évènements : Affectation Support
# ================================ #


def affecter_support_evenement():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        verifier_gestion(utilisateur_connecte)

        evenement_id = saisir_evenement_id()
        evenement = recherche_evenement(
            session,
            evenement_id,
        )

        afficher_evenement(evenement)

        numero_support = saisir_numero_support()
        support = recherche_collaborateur(
            session,
            numero_support,
        )

        affecter_support(
            evenement,
            support,
        )

        session.commit()

        evenement_id = evenement.id

    except (ValueError, PermissionError) as erreur:
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message(
        f"Un membre du Support a été affecté à l'évènement {evenement_id}."
    )


# ================================ #
# Contrôleur évènements : Évènements du Support
# ================================ #


def consulter_mes_evenements_support():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        verifier_authentification(utilisateur_connecte)

        evenements = evenements_affectes_support(
            session,
            utilisateur_connecte,
        )

        afficher_evenements(evenements)

    except (ValueError, PermissionError) as erreur:
        afficher_message(str(erreur))

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


# ================================ #
# Contrôleur évènements : Modification
# ================================ #


def modifier_evenement():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        evenement_id = saisir_evenement_id()
        evenement = recherche_evenement(
            session,
            evenement_id,
        )

        # Seul le Support responsable peut modifier l'évènement
        verifier_modif_evenement(
            utilisateur_connecte,
            evenement,
        )

        afficher_evenement(evenement)

        (
            nom,
            date_debut,
            date_fin,
            lieu,
            nombre_participants,
            notes,
        ) = saisir_modifications_evenement()

        modification_evenement(
            evenement,
            nom,
            date_debut,
            date_fin,
            lieu,
            nombre_participants,
            notes,
        )

        session.commit()

        evenement_id = evenement.id

    except (ValueError, PermissionError) as erreur:
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message(f"L'évènement {evenement_id} a été modifié.")
