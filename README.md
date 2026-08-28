# Epic Events CRM

Projet 12 de la formation Développeur d’application Python d’OpenClassrooms.

Réalisé par Marion LARUE.

## Description

Epic Events CRM est une application en ligne de commande permettant de gérer une clientèle, des contrats et des événements de l’entreprise Epic Events.

L’application utilise Python, SQLAlchemy et PostgreSQL.

## État du projet

Fonctionnalités actuellement développées :

- Connexion à PostgreSQL
- Modèles et relations SQLAlchemy
- Création des tables
- Schéma de la base de données
- Matrice des permissions

- [...]

## Installation

Prérequis :

- Python 3.11 ;
- PostgreSQL 17 ;
- Git.

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

Créer une base PostgreSQL nommée `epic_events_db` ainsi qu’un utilisateur dédié sans privilèges administratifs.

Copier le fichier d’exemple :

```powershell
Copy-Item .env.example .env
```

Compléter ensuite les variables dans `.env` :

```dotenv
DB_NAME=epic_events_db
DB_USER=epic_events_app
DB_PASSWORD=mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

ATTENTION : Le fichier `.env` contient des informations sensibles et ne doit jamais être publié.

## Utilisation

Création des tables absentes :

```powershell
python create_tables.py
```

Vérifier la connexion à PostgreSQL :

```powershell
python main.py
```

## Qualité du code

```powershell
black .
flake8 .
```