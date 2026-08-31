from pwinput import pwinput

# ================================
# Vue — Entrées des informations d'un collaborateur
# ================================


def saisir_infos_collaborateur():
    # Saisie du nom et de l'email
    nom = input("Nom : ").strip()
    email = input("Email : ").strip()

    # Affiche une étoile par caractère du MDP
    mdp = pwinput("Mot de passe : ", mask="*")

    # Confirme le MDP avec le même affichage masqué
    confirmation_mdp = pwinput("Confirmer le mot de passe : ", mask="*")

    # Transmet les quatre saisies
    return nom, email, mdp, confirmation_mdp


# ================================
# Vue — Messages concernant les collaborateurs
# ================================


def afficher_message(message):
    # Affiche le résultat transmis par le contrôleur
    print(message)
