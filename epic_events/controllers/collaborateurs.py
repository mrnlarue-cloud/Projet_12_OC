from epic_events.database import SessionLocale
from epic_events.models.collaborateur import (
    creation_collaborateur,
    creation_premier_gestionnaire,
    liste_collaborateurs,
    modification_collaborateur,
    recherche_collaborateur,
    suppression_collaborateur,
)
from epic_events.security.authentification import authentification_collaborateurs
from epic_events.security.permissions import verifier_gestion
from epic_events.views.collaborateurs import (
    afficher_collaborateur,
    afficher_collaborateurs,
    afficher_message,
    confirmer_suppression,
    saisir_departement,
    saisir_identifiants,
    saisir_infos_collaborateur,
    saisir_modifications_collaborateur,
    saisir_numero_employe,
)

# ================================ #
# Contrôleur collaborateurs : Création du premier compte Gestion
# ================================ #


def creer_premier_compte_gestion():
    # Récupère les infos saisies
    nom, email, mdp, confirmation_mdp = saisir_infos_collaborateur()

    # Ouvre une session avec la DB
    session = SessionLocale()

    try:
        # Prépare le premier compte
        creation_premier_gestionnaire(
            session,
            nom,
            email,
            mdp,
            confirmation_mdp,
        )

        # Enregistre dans Postgre
        session.commit()

    except Exception:
        # Annule les changements en cas d'erreur
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message("Compte Gestion créé avec succès.")


# ================================ #
# Contrôleur collaborateurs : Consultation des collaborateurs
# ================================ #


def consulter_collaborateurs():
    # Récupère les ID
    email_connexion, mdp_connexion = saisir_identifiants()

    # Ouvre une session avec la DB
    session = SessionLocale()

    try:
        # Authentifie l'utilisateur
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email_connexion,
            mdp_connexion,
        )

        # Vérifie les droits
        verifier_gestion(utilisateur_connecte)

        # Récupère la liste
        collaborateurs = liste_collaborateurs(session)

        # Affiche les collaborateurs
        afficher_collaborateurs(collaborateurs)

    except (ValueError, PermissionError) as erreur:
        # Affiche le refus
        afficher_message(str(erreur))

    except Exception:
        # Annule et conserve l'erreur technique
        session.rollback()
        raise

    finally:
        session.close()


# ================================ #
# Contrôleur collaborateurs : Création d'un collaborateur
# ================================ #


def creer_collaborateur():
    # Récupère les ID
    email_connexion, mdp_connexion = saisir_identifiants()

    # Ouvre une session avec la DB
    session = SessionLocale()

    try:
        # Authentifie l'utilisateur
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email_connexion,
            mdp_connexion,
        )

        # Vérifie les droits
        verifier_gestion(utilisateur_connecte)

        # Récupère les infos du nouveau compte
        nom, email, mdp, confirmation_mdp = saisir_infos_collaborateur()
        nom_departement = saisir_departement()

        # Prépare le collaborateur
        nouveau_collaborateur = creation_collaborateur(
            session,
            nom,
            email,
            mdp,
            confirmation_mdp,
            nom_departement,
        )

        # Enregistre dans Postgre
        session.commit()

        # Conserve le numéro avant de fermer la session
        numero_employe = nouveau_collaborateur.numero_employe

    except (ValueError, PermissionError) as erreur:
        # Annule et affiche le refus
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        # Annule et conserve l'erreur technique
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message(f"Le collaborateur {numero_employe} a été créé.")


# ================================ #
# Contrôleur collaborateurs : Modification d'un collaborateur
# ================================ #


def modifier_collaborateur():
    # Récupère les ID
    email_connexion, mdp_connexion = saisir_identifiants()

    # Ouvre une session avec la DB
    session = SessionLocale()

    try:
        # Authentifie l'utilisateur
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email_connexion,
            mdp_connexion,
        )

        # Vérifie les droits
        verifier_gestion(utilisateur_connecte)

        # Récupère le numéro employé
        numero_employe = saisir_numero_employe()

        # Cherche le collaborateur
        collaborateur = recherche_collaborateur(
            session,
            numero_employe,
        )

        # Affiche le compte sélectionné
        afficher_collaborateur(collaborateur)

        # Récupère les nouvelles infos
        (
            nom,
            email,
            mdp,
            confirmation_mdp,
            nom_departement,
        ) = saisir_modifications_collaborateur()

        # Modifie le collaborateur
        modification_collaborateur(
            session,
            collaborateur,
            nom,
            email,
            mdp,
            confirmation_mdp,
            nom_departement,
        )

        # Enregistre dans Postgre
        session.commit()

    except (ValueError, PermissionError) as erreur:
        # Annule et affiche le refus
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        # Annule et conserve l'erreur technique
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message("Le collaborateur a été modifié.")


# ================================ #
# Contrôleur collaborateurs : Suppression d'un collaborateur
# ================================ #


def supprimer_collaborateur():
    # Récupère les ID
    email_connexion, mdp_connexion = saisir_identifiants()

    # Ouvre une session avec la DB
    session = SessionLocale()

    try:
        # Authentifie l'utilisateur
        utilisateur_connecte = authentification_collaborateurs(
            session,
            email_connexion,
            mdp_connexion,
        )

        # Vérifie les droits
        verifier_gestion(utilisateur_connecte)

        # Récupère le numéro employé
        numero_employe = saisir_numero_employe()

        # Cherche le collaborateur
        collaborateur = recherche_collaborateur(
            session,
            numero_employe,
        )

        # Affiche le compte sélectionné
        afficher_collaborateur(collaborateur)

        # Annule si la suppression n'est pas confirmée
        if not confirmer_suppression():
            afficher_message("Suppression annulée.")
            return

        # Prépare la suppression
        suppression_collaborateur(
            session,
            collaborateur,
        )

        # Enregistre dans Postgre
        session.commit()

    except (ValueError, PermissionError) as erreur:
        # Annule et affiche le refus
        session.rollback()
        afficher_message(str(erreur))
        return

    except Exception:
        # Annule et conserve l'erreur technique
        session.rollback()
        raise

    finally:
        session.close()

    afficher_message("Le collaborateur a été supprimé.")
