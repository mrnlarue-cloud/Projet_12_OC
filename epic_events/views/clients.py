# ================================ #
# Vue clients : Saisies
# ================================ #


def saisir_infos_client():
    nom_complet = input("Nom complet : ").strip()
    email = input("Email : ").strip()
    telephone = input("Téléphone : ").strip()
    entreprise = input("Entreprise : ").strip()
    date_creation_contact = input("Date du premier contact (JJ/MM/AAAA) : ").strip()
    date_dernier_echange = input("Date du dernier échange (JJ/MM/AAAA) : ").strip()

    return (
        nom_complet,
        email,
        telephone,
        entreprise,
        date_creation_contact,
        date_dernier_echange,
    )


def saisir_client_id():
    return input("ID du client : ").strip()


# ================================ #
# Vue clients : Modifications
# ================================ #


def saisir_modifications_client():
    print("Laissez le champ vide pour conserver sa valeur actuelle.")

    nom_complet = input("Nouveau nom complet : ").strip()
    email = input("Nouvel email : ").strip()
    telephone = input("Nouveau téléphone : ").strip()
    entreprise = input("Nouvelle entreprise : ").strip()
    date_creation_contact = input(
        "Nouvelle date du premier contact (JJ/MM/AAAA) : "
    ).strip()
    date_dernier_echange = input(
        "Nouvelle date du dernier échange (JJ/MM/AAAA) : "
    ).strip()

    return (
        nom_complet,
        email,
        telephone,
        entreprise,
        date_creation_contact,
        date_dernier_echange,
    )


# ================================ #
# Vue clients : Affichage
# ================================ #


def afficher_client(client):
    print(
        f"\nClient {client.id}"
        f"\nNom : {client.nom_complet}"
        f"\nEmail : {client.email}"
        f"\nTéléphone : {client.telephone}"
        f"\nEntreprise : {client.entreprise}"
        f"\nPremier contact : "
        f"{client.date_creation_contact.strftime('%d/%m/%Y')}"
        f"\nDernier échange : "
        f"{client.date_dernier_echange.strftime('%d/%m/%Y')}"
        f"\nCommercial : {client.commercial.nom}\n"
    )


def afficher_clients(clients):
    if not clients:
        print("Aucun client enregistré.")
        return

    for client in clients:
        afficher_client(client)


def afficher_message(message):
    print(message)
