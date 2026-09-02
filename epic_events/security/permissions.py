# ================================ #
# Authentification obligatoire
# ================================ #


def verifier_authentification(collaborateur):
    # Refus d'un utilisateur non authentifié
    if collaborateur is None:
        raise PermissionError("Vous devez impérativement être connecté.")


# ================================ #
# Permissions du département Gestion
# ================================ #


def verifier_gestion(collaborateur):
    verifier_authentification(collaborateur)

    # Refus des collaborateurs d'autres départements
    if collaborateur.departement.nom != "Gestion":
        raise PermissionError("Cette action est réservée au département Gestion.")


# ================================ #
# Permissions du département Commercial
# ================================ #


def verifier_commercial(collaborateur):
    verifier_authentification(collaborateur)

    # Refus des collaborateurs d'autres départements
    if collaborateur.departement.nom != "Commercial":
        raise PermissionError("Cette action est réservée au département Commercial.")


# ================================ #
# Modification d'un client
# ================================ #


def verifier_modif_client(collaborateur, client):
    verifier_commercial(collaborateur)

    # Refus si le commercial n'est pas responsable du client
    if client.commercial_id != collaborateur.numero_employe:
        raise PermissionError("Vous ne pouvez modifier que vos propres clients.")
