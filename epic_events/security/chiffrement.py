# ================================ #
# Imports
# ================================ #


from os import getenv

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from sqlalchemy import Text
from sqlalchemy.types import TypeDecorator
from datetime import date

# ================================ #
# Clé de chiffrement
# ================================ #

# Récupération de la clé dans .env
load_dotenv()
cle = getenv("FERNET_KEY")

# Initialisation de Fernet avec la clé
fernet = Fernet(cle.encode())


# ================================ #
# Chiffrement des données
# ================================ #


class TexteChiffre(TypeDecorator):
    # Stockage sous forme de texte en BDD
    impl = Text
    cache_ok = True

    # Chiffrement avant enregistrement
    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return fernet.encrypt(value.encode()).decode()

    # Déchiffrement après lecture
    def process_result_value(self, value, dialect):
        if value is None:
            return None

        return fernet.decrypt(value.encode()).decode()


# ================================ #
# Chiffrement des dates
# ================================ #


class DateChiffree(TypeDecorator):
    impl = Text
    cache_ok = True

    # Conversion de la date en texte puis chiffrement
    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return fernet.encrypt(value.isoformat().encode()).decode()

    # Déchiffrement et reconversion en date
    def process_result_value(self, value, dialect):
        if value is None:
            return None

        date_texte = fernet.decrypt(value.encode()).decode()
        return date.fromisoformat(date_texte)
