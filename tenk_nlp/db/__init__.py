import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

load_dotenv()


db_config = {
    "driver": os.getenv("DB_DRIVER"),
    "username": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
}

if db_config["driver"] == "sqlite":
    DSN = f"{db_config['driver']}:////{db_config['host']}"

else:

    DSN = URL.create(
        os.getenv("DB_DRIVER"),
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
    )

engine = create_engine(DSN, echo=True)
