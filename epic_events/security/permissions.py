# ================================ #
# Permissions du département Gestion
# ================================ #


def verifier_gestion(collaborateur):
    # Refus d'un utilisateur non authentifié
    if collaborateur is None:
        raise PermissionError("Vous devez impérativement être connecté.")

    # Refus des collaborateurs d'autres départements
    if collaborateur.departement.nom != "Gestion":
        raise PermissionError("Cette action est réservée au département Gestion.")
