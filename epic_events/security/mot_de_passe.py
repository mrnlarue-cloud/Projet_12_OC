from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# ================================ #
# Gestion des mots de passe
# ================================ #

# Crée l'outil de hash d'Argon2 pour MDP
outil_mdp = PasswordHasher()


def hash_mdp(mdp):
    # Modification du MDP en hash
    return outil_mdp.hash(mdp)


def verification_mdp(mdp_hash, mdp):
    try:
        # Compare le mdp avec le hash enregistré
        outil_mdp.verify(mdp_hash, mdp)
        return True
    except VerifyMismatchError:
        # Un mauvais match de mdp provoque une erreur
        return False
