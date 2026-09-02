from pwinput import pwinput

# ================================ #
# Vue collaborateurs : Saisie des identifiants
# ================================ #


def saisir_identifiants():
    # Saisie de l'email
    email = input("Email de connexion : ").strip()
    # Saisie du MDP avec *
    mdp = pwinput("Mot de passe : ", mask="*")
    # Transmission des identifiants
    return email, mdp


# ================================ #
# Vue collaborateurs : Saisie d'un collaborateur
# ================================ #


def saisir_infos_collaborateur():
    nom = input("Nom : ").strip()
    email = input("Email : ").strip()
    # Saisie & confirmation du MDP
    mdp = pwinput("Mot de passe : ", mask="*")
    confirmation_mdp = pwinput("Confirmer le mot de passe : ", mask="*")
    # Transmissions des informations saisies
    return nom, email, mdp, confirmation_mdp


# ================================ #
# Vue collaborateurs : Saisie du département
# ================================ #


def saisir_departement():
    # Transmission du département saisi
    return input("Département (Gestion, Commercial ou Support) : ").strip()


# ================================ #
# Vue collaborateurs : Sélection d'un collaborateur
# ================================ #


def saisir_numero_employe():
    # Transmission du numéro employé saisi
    return input("Numéro employé : ").strip()


# ================================ #
# Vue collaborateurs : Modification d'un collaborateur
# ================================ #


def saisir_modifications_collaborateur():
    # Conservation des informations actuelles
    print("Laissez un champ vide pour conserver sa valeur actuelle.")

    # Saisie des nouvelles informations
    nom = input("Nouveau nom : ").strip()
    email = input("Nouvel email : ").strip()
    mdp = pwinput("Nouveau mot de passe : ", mask="*")
    confirmation_mdp = pwinput("Confirmer le nouveau mot de passe : ", mask="*")
    nom_departement = input("Nouveau département : ").strip()

    # Transmet les informations saisies
    return nom, email, mdp, confirmation_mdp, nom_departement


# ================================ #
# Vue collaborateurs : Confirmation d'une suppression
# ================================ #


def confirmer_suppression():
    # Récupère la confirmation de l'utilisateur
    reponse = input("Confirmer la suppression ? (OUI/NON) : ").strip()

    # Confirme uniquement avec la réponse o
    return reponse == "OUI"


# ================================ #
# Vue collaborateurs : Affichage des collaborateurs
# ================================ #


def afficher_collaborateur(collaborateur):
    # Affiche les informations principales du collaborateur
    print(
        f"{collaborateur.numero_employe} — "
        f"{collaborateur.nom} — "
        f"{collaborateur.email} — "
        f"{collaborateur.departement.nom}"
    )


def afficher_collaborateurs(collaborateurs):
    if not collaborateurs:
        print("Aucun collaborateur enregistré.")
        return

    # Affiche chaque collaborateur
    for collaborateur in collaborateurs:
        afficher_collaborateur(collaborateur)


# ================================ #
# Vue collaborateurs : Messages concernant les collaborateurs
# ================================ #


def afficher_message(message):
    # Affiche le message transmis par le contrôleur
    print(message)
