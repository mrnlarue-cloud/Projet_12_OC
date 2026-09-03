# ================================ #
# Vue contrats : Saisies
# ================================ #


def saisir_infos_contrat():
    client_id = input("ID du client : ").strip()
    montant_total = input("Montant total : ").strip()
    montant_restant = input("Montant restant : ").strip()
    date_creation = input("Date de création (JJ/MM/AAAA) : ").strip()
    signature = input("Contrat signé (OUI/NON) : ").strip()

    return (
        client_id,
        montant_total,
        montant_restant,
        date_creation,
        signature,
    )


def saisir_contrat_id():
    return input("ID du contrat : ").strip()


# ================================ #
# Vue contrats : Modifications
# ================================ #


def saisir_modifications_contrat():
    print("Laissez le champ vide pour conserver sa valeur actuelle.")

    montant_total = input("Nouveau montant total : ").strip()
    montant_restant = input("Nouveau montant restant : ").strip()
    date_creation = input("Nouvelle date de création (JJ/MM/AAAA) : ").strip()
    signature = input("Nouveau statut de signature (OUI/NON) : ").strip()

    return (
        montant_total,
        montant_restant,
        date_creation,
        signature,
    )


# ================================ #
# Vue contrats : Affichage
# ================================ #


def afficher_contrat(contrat):
    # Présentation lisible du booléen stocké en DB
    signature = "OUI" if contrat.signature else "NON"

    print(
        f"\nContrat {contrat.id}"
        f"\nClient : {contrat.client.nom_complet}"
        f"\nCommercial : {contrat.commercial.nom}"
        f"\nMontant total : {contrat.montant_total:.2f} €"
        f"\nMontant restant : {contrat.montant_restant:.2f} €"
        f"\nDate de création : "
        f"{contrat.date_creation.strftime('%d/%m/%Y')}"
        f"\nSigné : {signature}\n"
    )


def afficher_contrats(contrats):
    if not contrats:
        print("Aucun contrat trouvé.")
        return

    for contrat in contrats:
        afficher_contrat(contrat)


def afficher_message(message):
    print(message)
