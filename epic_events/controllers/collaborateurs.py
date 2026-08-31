from epic_events.database import SessionLocale
from epic_events.models.collaborateur import creation_premier_gestionnaire
from epic_events.views.collaborateurs import (
    afficher_message,
    saisir_infos_collaborateur,
)

# ================================ #
# Contrôleur — Création du premier compte Gestion
# ================================ #


def creer_premier_compte_gestion():
    # Demande les informations à la vue
    nom, email, mdp, confirmation_mdp = saisir_infos_collaborateur()

    # Ouvre une session pour travailler avec la DB
    session = SessionLocale()

    try:
        # Demande au modèle de vérifier et préparer le compte
        creation_premier_gestionnaire(session, nom, email, mdp, confirmation_mdp)

        # Confirme l'enregistrement dans PostgreSQL
        session.commit()

    except Exception:
        # Annule les changements non confirmés si une erreur survient
        session.rollback()

        # Transmet l'erreur pour connaître la cause
        raise

    finally:
        # Ferme la session, que l'opération ait réussi ou échoué
        session.close()

    # Affiche la confirmation uniquement après une réussite
    afficher_message("Les départements et le premier compte Gestion sont prêts.")
