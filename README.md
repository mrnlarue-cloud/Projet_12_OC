# Epic Events CRM

Projet 12 de la formation Développeur d’application Python d’OpenClassrooms.

Réalisé par Marion LARUE.

Repository GitHub : https://github.com/mrnlarue-cloud/Projet_12_OC

## Description

Epic Events CRM est une application en ligne de commande permettant de gérer les collaborateurs, les clients, les contrats et les évènements de l’entreprise Epic Events.

L’application utilise Python, SQLAlchemy et PostgreSQL.

## État du projet

Fonctionnalités terminées :

- Connexion à PostgreSQL
- Modèles et relations SQLAlchemy
- Création des tables
- Schéma de la base de données
- Matrice des permissions
- Hachage et vérification des mots de passe avec Argon2
- Authentification des collaborateurs
- Permissions selon les départements
- Création, consultation, modification et suppression des collaborateurs
- Création, consultation et modification des clients
- Association automatique d’un client au Commercial connecté
- Création, consultation et modification des contrats
- Filtres des contrats non signés et non soldés
- Création, consultation et modification des évènements selon les permissions
- Affectation d’un collaborateur Support à un évènement
- Filtres des évènements sans Support et des évènements attribués au Support connecté
- Menu principal de l’application
- Journalisation des erreurs techniques avec Sentry

## Architecture

L’application utilise une architecture « fat models, skinny views ».

- Les modèles contiennent les requêtes SQLAlchemy et les règles métier
- Les vues recueillent les saisies et affichent les résultats dans la console
- Les contrôleurs coordonnent l’authentification, les permissions, les modèles et les transactions
- Le package de sécurité contient l’authentification, les permissions et la gestion des mots de passe

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

tests/
├── test_authentification.py
├── test_collaborateurs.py
├── test_mdp.py
└── test_permissions.py

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
```

Le fichier `.env` contient des informations sensibles et ne doit jamais être ajouté au dépôt Git.

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

## Qualité du code

Formater le code :

```powershell
black .
```

Vérifier le respect des règles de style :

```powershell
flake8 .
```