from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


load_dotenv()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=getenv("DB_USER"),
    password=getenv("DB_PASSWORD"),
    host=getenv("DB_HOST"),
    port=int(getenv("DB_PORT", "5432")),
    database=getenv("DB_NAME"),
)

engine = create_engine(database_url)