# Matrice des permissions

Toutes les actions nécessitent une authentification.

- Action : Consulter les clients.
  - Gestion : Autorisée.
  - Commercial : Autorisée.
  - Support : Autorisée.

- Action : Consulter les contrats.
  - Gestion : Autorisée.
  - Commercial : Autorisée.
  - Support : Autorisée.

- Action : Consulter les événements.
  - Gestion : Autorisée.
  - Commercial : Autorisée.
  - Support : Autorisée.

- Action : Créer un collaborateur.
  - Gestion : Autorisée.
  - Commercial : Interdite.
  - Support : Interdite.

- Action : Modifier ou supprimer un collaborateur, y compris son département.
  - Gestion : Autorisée.
  - Commercial : Interdite.
  - Support : Interdite.

- Action : Créer un client.
  - Gestion : Interdite.
  - Commercial : Autorisée avec association automatique au commercial connecté.
  - Support : Interdite.

- Action : Modifier un client.
  - Gestion : Interdite.
  - Commercial : Autorisée uniquement pour ses propres clients.
  - Support : Interdite.

- Action : Créer un contrat.
  - Gestion : Autorisée.
  - Commercial : Interdite.
  - Support : Interdite.

- Action : Modifier un contrat.
  - Gestion : Autorisée pour tous les contrats.
  - Commercial : Autorisée uniquement pour les contrats de ses clients.
  - Support : Interdite.

- Action : Créer un événement.
  - Gestion : Interdite.
  - Commercial : Autorisée pour l’un de ses clients si le contrat est signé.
  - Support : Interdite.

- Action : Affecter un collaborateur support à un événement.
  - Gestion : Autorisée.
  - Commercial : Interdite.
  - Support : Interdite.

- Action : Modifier un événement.
  - Gestion : Autorisée uniquement pour affecter un support.
  - Commercial : Interdite.
  - Support : Autorisée uniquement pour les événements qui lui sont attribués.

- Action : Afficher les événements sans support.
  - Gestion : Autorisée.
  - Commercial : Non prévue.
  - Support : Non prévue.

- Action : Afficher les contrats non signés ou non entièrement payés.
  - Gestion : Non prévue.
  - Commercial : Autorisée.
  - Support : Non prévue.

- Action : Afficher ses événements attribués.
  - Gestion : Non prévue.
  - Commercial : Non prévue.
  - Support : Autorisée.

- Action : Supprimer un client, un contrat ou un événement.
  - Gestion : Interdite.
  - Commercial : Interdite.
  - Support : Interdite.

## Principe général

Toute action qui n’est pas explicitement autorisée doit être refusée.