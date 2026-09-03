from epic_events.database import SessionLocale
from epic_events.models.clients import recherche_client
from epic_events.models.contrats import (
    contrats_non_signes,
    contrats_non_soldes,
    creation_contrat,
    liste_contrats,
    modification_contrat,
    recherche_contrat,
)
from epic_events.security.authentification import authentification_collaborateurs
from epic_events.security.permissions import (
    verifier_authentification,
    verifier_commercial,
    verifier_gestion,
    verifier_modif_contrat,
)
from epic_events.views.collaborateurs import saisir_identifiants
from epic_events.views.contrats import (
    afficher_contrat,
    afficher_contrats,
    afficher_message,
    saisir_contrat_id,
    saisir_infos_contrat,
    saisir_modifications_contrat,
)

# ================================ #
# Contrôleur contrats : Consultation
# ================================ #


def consulter_contrats():
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

        contrats = liste_contrats(session)
        afficher_contrats(contrats)

    except (ValueError, PermissionError) as erreur:
        afficher_message(str(erreur))

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


# ================================ #
# Contrôleur contrats : Création
# ================================ #


def creer_contrat():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        # La création est réservée à Gestion
        verifier_gestion(utilisateur_connecte)

        (
            client_id,
            montant_total,
            montant_restant,
            date_creation,
            signature,
        ) = saisir_infos_contrat()

        client = recherche_client(
            session,
            client_id,
        )

        # Le modèle reprend le Commercial responsable du client
        nouveau_contrat = creation_contrat(
            session,
            client,
            montant_total,
            montant_restant,
            date_creation,
            signature,
        )

        session.commit()

        # Conserve l'ID avant la fermeture de la session
        contrat_id = nouveau_contrat.id

    except (ValueError, PermissionError) as erreur:
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message(f"Le contrat {contrat_id} a été créé.")


# ================================ #
# Contrôleur contrats : Modification
# ================================ #


def modifier_contrat():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        verifier_authentification(utilisateur_connecte)

        contrat_id = saisir_contrat_id()
        contrat = recherche_contrat(
            session,
            contrat_id,
        )

        # La permission dépend du contrat sélectionné
        verifier_modif_contrat(
            utilisateur_connecte,
            contrat,
        )

        afficher_contrat(contrat)

        (
            montant_total,
            montant_restant,
            date_creation,
            signature,
        ) = saisir_modifications_contrat()

        modification_contrat(
            contrat,
            montant_total,
            montant_restant,
            date_creation,
            signature,
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

    afficher_message("Le contrat a été modifié.")


# ================================ #
# Contrôleur contrats : Filtres
# ================================ #


def consulter_contrats_non_signes():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        # Ces filtres sont réservés au département Commercial
        verifier_commercial(utilisateur_connecte)

        contrats = contrats_non_signes(session)
        afficher_contrats(contrats)

    except (ValueError, PermissionError) as erreur:
        afficher_message(str(erreur))

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def consulter_contrats_non_soldes():
    email, mdp = saisir_identifiants()
    session = SessionLocale()

    try:
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email,
            mdp,
        )

        # Ces filtres sont réservés au département Commercial
        verifier_commercial(utilisateur_connecte)

        contrats = contrats_non_soldes(session)
        afficher_contrats(contrats)

    except (ValueError, PermissionError) as erreur:
        afficher_message(str(erreur))

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()
