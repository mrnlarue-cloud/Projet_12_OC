# ================================ #
# Accès réservé aux utilisateurs/collaborateurs authentifiés
# ================================ #


def verifier_authentification(collaborateur):
    # Refus d'un utilisateur non authentifié
    if collaborateur is None:
        raise PermissionError("Vous devez impérativement être connecté.")


# ================================ #
# Accès réservé au département Gestion
# ================================ #


def verifier_gestion(collaborateur):
    verifier_authentification(collaborateur)

    # Refus des collaborateurs d'autres départements
    if collaborateur.departement.nom != "Gestion":
        raise PermissionError("Cette action est réservée au département Gestion.")


# ================================ #
# Accès réservé au département Commercial
# ================================ #


def verifier_commercial(collaborateur):
    verifier_authentification(collaborateur)

    # Refus des collaborateurs d'autres départements
    if collaborateur.departement.nom != "Commercial":
        raise PermissionError("Cette action est réservée au département Commercial.")


# ================================ #
# Création d'un évènement par son Commercial
# ================================ #


def verifier_creation_evenement(collaborateur, contrat):
    verifier_commercial(collaborateur)

    # Le Commercial doit être responsable du contrat
    if contrat.commercial_id != collaborateur.numero_employe:
        raise PermissionError(
            "Vous ne pouvez créer un évènement que pour l'un de vos clients."
        )


# ================================ #
# Modification d'un client par son collaborateur Commercial
# ================================ #


def verifier_modif_client(collaborateur, client):
    verifier_commercial(collaborateur)

    # Refus si le commercial n'est pas responsable du client
    if client.commercial_id != collaborateur.numero_employe:
        raise PermissionError("Vous ne pouvez modifier que vos propres clients.")


# ================================ #
# Modification des contrats selon le rôle du collaborateur
# ================================ #


def verifier_modif_contrat(collaborateur, contrat):
    verifier_authentification(collaborateur)

    # Gestion peut modifier tous les contrats
    if collaborateur.departement.nom == "Gestion":
        return

    # Les autres rôles ne peuvent pas modifier les contrats
    if collaborateur.departement.nom != "Commercial":
        raise PermissionError(
            "Cette action est réservée aux départements Gestion et Commercial."
        )

    # Un Commercial est limité aux contrats de ses propres clients
    if contrat.commercial_id != collaborateur.numero_employe:
        raise PermissionError(
            "Vous ne pouvez modifier que les contrats de vos clients."
        )


# ================================ #
# Modification d'un évènement par son collaborateur Support
# ================================ #


def verifier_modif_evenement(collaborateur, evenement):
    verifier_authentification(collaborateur)

    # La modif est réservée au département Support
    if collaborateur.departement.nom != "Support":
        raise PermissionError("Cette action est réservée au département Support.")

    # Le Support doit être responsable de l'évènement
    if evenement.support_id != collaborateur.numero_employe:
        raise PermissionError(
            "Vous ne pouvez modifier que les évènements qui vous sont affectés."
        )
