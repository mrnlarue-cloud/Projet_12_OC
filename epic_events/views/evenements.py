# ================================ #
# Vue évènements : Saisies
# ================================ #


def saisir_infos_evenement():
    # Informations obligatoires pour créer l'évènement
    contrat_id = input("ID du contrat : ").strip()
    nom = input("Nom de l'évènement : ").strip()
    date_debut = input("Date et heure de début (JJ/MM/AAAA HH:MM) : ").strip()
    date_fin = input("Date et heure de fin (JJ/MM/AAAA HH:MM) : ").strip()
    lieu = input("Lieu : ").strip()
    nombre_participants = input("Nombre de participants : ").strip()
    notes = input("Notes : ").strip()

    return (
        contrat_id,
        nom,
        date_debut,
        date_fin,
        lieu,
        nombre_participants,
        notes,
    )


def saisir_evenement_id():
    return input("ID de l'évènement : ").strip()


def saisir_numero_support():
    return input("Numéro employé du Support : ").strip()


# ================================ #
# Vue évènements : Modifications
# ================================ #


def saisir_modifications_evenement():
    print("Laissez le champ vide pour conserver sa valeur actuelle.")

    nom = input("Nouveau nom : ").strip()
    date_debut = input("Nouvelle date et heure de début (JJ/MM/AAAA HH:MM) : ").strip()
    date_fin = input("Nouvelle date et heure de fin (JJ/MM/AAAA HH:MM) : ").strip()
    lieu = input("Nouveau lieu : ").strip()
    nombre_participants = input("Nouveau nombre de participants : ").strip()
    notes = input("Nouvelles notes : ").strip()

    return (
        nom,
        date_debut,
        date_fin,
        lieu,
        nombre_participants,
        notes,
    )


# ================================ #
# Vue évènements : Affichage
# ================================ #


def afficher_evenement(evenement):
    # L'évènement peut exister avant son affectation à un Support !
    support = evenement.support.nom if evenement.support else "Non affecté"

    print(
        f"\nÉvènement {evenement.id}"
        f"\nNom : {evenement.nom}"
        f"\nContrat : {evenement.contrat_id}"
        f"\nClient : {evenement.contrat.client.nom_complet}"
        f"\nDébut : {evenement.date_debut.strftime('%d/%m/%Y %H:%M')}"
        f"\nFin : {evenement.date_fin.strftime('%d/%m/%Y %H:%M')}"
        f"\nSupport : {support}"
        f"\nLieu : {evenement.lieu}"
        f"\nParticipants : {evenement.nombre_participants}"
        f"\nNotes : {evenement.notes}\n"
    )


def afficher_evenements(evenements):
    if not evenements:
        print("Aucun évènement trouvé.")
        return

    for evenement in evenements:
        afficher_evenement(evenement)


def afficher_message(message):
    print(message)
