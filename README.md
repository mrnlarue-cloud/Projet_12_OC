# Epic Events CRM

Projet 12 de la formation Développeur d’application Python d’OpenClassrooms.

Réalisé par Marion LARUE.

Repository GitHub : https://github.com/mrnlarue-cloud/Projet_12_OC

## Description

Epic Events CRM est une application en ligne de commande permettant de gérer les collaborateurs, les clients, les contrats et les évènements de l’entreprise Epic Events.

L’application utilise Python, SQLAlchemy et PostgreSQL.

## Architecture

L’application utilise une architecture « fat models, skinny views ».

- Les modèles contiennent les requêtes SQLAlchemy et les règles métier
- Les vues recueillent les saisies et affichent les résultats dans la console
- Les contrôleurs coordonnent l’authentification, les permissions, les modèles et les transactions
- Le package de sécurité contient l’authentification, les permissions, le chiffrement des données et la gestion des mots de passe

### Organisation finale des fichiers

```text
epic_events/
├── controllers/
│   ├── collaborateurs.py
│   ├── clients.py
│   ├── contrats.py
│   └── evenements.py
├── models/
│   ├── departement.py
│   ├── collaborateur.py
│   ├── clients.py
│   ├── contrats.py
│   └── evenements.py
├── security/
│   ├── authentification.py
│   ├── chiffrement.py
│   ├── mot_de_passe.py
│   └── permissions.py
├── views/
│   ├── collaborateurs.py
│   ├── clients.py
│   ├── contrats.py
│   └── evenements.py
└── database.py

docs/
├── matrice_permissions.md
└── schema-base-donnees.svg

create_tables.py
main.py
requirements.txt
.env.example
README.md
```

## Installation

Prérequis :

- Python 3.11
- PostgreSQL 17
- Git

Créer et activer l’environnement virtuel :

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
```

## Configuration

Créer une base de données PostgreSQL nommée `epic_events_db` ainsi qu’un utilisateur dédié sans droits administratifs.

Copier le fichier d’exemple :

```powershell
Copy-Item .env.example .env
```

Compléter les variables dans `.env` :

```dotenv
DB_NAME=epic_events_db
DB_USER=epic_events_app
DB_PASSWORD=mot_de_passe
DB_HOST=localhost
DB_PORT=5432
SENTRY_DSN=votre_dsn_sentry
FERNET_KEY=votre_cle_fernet
```

Générer une clé Fernet avec la commande :

```powershell
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Conserver cette clé dans `.env` pour permettre le déchiffrement des données enregistrées.

Le fichier `.env` contient des informations sensibles et ne doit jamais être ajouté au dépôt Git.

## Chiffrement des données

L'application utilise Fernet, via la bibliothèque `cryptography`, pour chiffrer les données avant leur enregistrement dans PostgreSQL et les déchiffrer lors de leur lecture.

Le fichier `epic_events/security/chiffrement.py` contient trois classes utilisant `TypeDecorator` de SQLAlchemy :

- `TexteChiffre` pour les informations textuelles.
- `DateChiffree` pour les dates.
- `MontantChiffre` pour les montants des contrats.

Le chiffrement concerne les informations personnelles des clients, les noms des collaborateurs, les montants et dates des contrats ainsi que les noms, lieux et notes des évènements.

Les identifiants, les clés étrangères et certains champs nécessaires au fonctionnement des recherches et des filtres restent en clair.

Les mots de passe des collaborateurs sont hachés séparément avec Argon2.

## Utilisation

Créer les tables absentes :

```powershell
python create_tables.py
```

Lancer l’application :

```powershell
python main.py
```

Le menu principal permet ensuite d’accéder à la gestion des collaborateurs, des clients, des contrats et des évènements.