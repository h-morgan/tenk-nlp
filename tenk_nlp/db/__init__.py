import os
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import URL, MetaData, create_engine, insert, select, update
from sqlalchemy.dialects.mysql import insert as myinsert
from sqlalchemy.orm.exc import NoResultFound

load_dotenv()


db_config = {
    "driver": os.getenv("DB_DRIVER"),
    "username": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
}

if db_config["driver"] == "sqlite":
    USE_SQLITE = True
    DSN = f"{db_config['driver']}:////{db_config['host']}"

else:
    USE_SQLITE = False
    DSN = URL.create(
        os.getenv("DB_DRIVER"),
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
    )

engine = create_engine(DSN)

metadata = MetaData()
metadata.reflect(engine)


class DataBase:
    def execute_query(self, query_stmt):
        with engine.begin() as conn:
            result = conn.execute(query_stmt)
            return result

    def upsert_company(self, company_data: dict[str, str | int | datetime]):
        table = metadata.tables["company"]

        # upsert syntax diff for mysql vs sqlite
        if USE_SQLITE:
            result = self._sqlite_upsert(table, company_data)

        else:
            stmt = myinsert(table).values(company_data)
            stmt = stmt.on_duplicate_key_update(company_data)
            result = self.execute_query(stmt)
        return result

    def _sqlite_upsert(self, table, data):

        # find if row exists with this id
        data_id = data["id"]
        find_stmt = select(table.c.id).where(table.c.id == data_id)
        try:
            row = self.execute_query(find_stmt).one()
            # now we know a row exists so update the values
            logger.debug(
                f"[{table.name}] Item with id {data_id} already exists, updating"
            )
            update_stmt = update(table).values(data).where(table.c.id == data_id)
            result = self.execute_query(update_stmt)
        except NoResultFound:
            # this means it's a new row, insert
            insert_stmt = insert(table).values(data)
            result = self.execute_query(insert_stmt)

        return result


database = DataBase()
