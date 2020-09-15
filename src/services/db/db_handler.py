"""
This script contains database handler
"""

from traceback import print_exc

import pandas as pd
from sqlalchemy import create_engine

from src.services.config.config_handler import ConfigHandler


class DbHandler:
    """
    Class containing database handler object.
    """

    def __init__(self):

        # Loading infra configuration file
        _config = ConfigHandler().infra_config

        conn_string = (
            f"postgresql://{_config.db.user}:{_config.db.password}@"
            f"{_config.db.host}:{_config.db.port}/{_config.db.database}"
        )
        self._engine = create_engine(conn_string)

    @property
    def connection(self):
        import psycopg2
        """Returns a connection to the database"""
        _config = ConfigHandler().infra_config
        return psycopg2.connect(
            host=_config.db.host,
            port=_config.db.port,
            user=_config.db.user,
            password=_config.db.password,
            database=_config.db.database,
        )

    def execute(self, sql):
        """Executes a SQL query

        :param sql : SQL query
        """
        import psycopg2
        connection = self.connection
        try:
            with connection.cursor() as cur:
                cur.execute(sql)
                connection.commit()
                print(sql)
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"\033[91mError: {error}\033[0m")
            print_exc()
        finally:
            cur.close()

    def write(self, df, table_name, *args, **kwargs):
        """Writes a DataFrame to the db

        :param df: pandas DataFrame to write
        :param table_name: name of the table
        """
        df.to_sql(name=table_name, con=self._engine, *args, **kwargs)

    def read(self, sql, *args, **kwargs):
        """Reads a DataFrame from a SQL query, using pd.read_sql

        :param sql: query to execute to retrieve the DataFrame
        :returns: the SQL table as a pandas DataFrame
        """
        return pd.read_sql(sql, self._engine, *args, **kwargs)
