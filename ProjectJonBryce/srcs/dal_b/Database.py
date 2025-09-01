import psycopg2
from config import Config


class Database:
    def __init__(self):
        """counstractor / בנאי"""
        self.conn = None
        self.cursor = None
        pass

    def getDataBaseConnection(self):
        """create connection to postgres sql and return cursor"""
        self.conn = psycopg2.connect(dbname=Config.DATABASE_DBNAME,
                                     user=Config.DATABASE_USER,
                                     port=Config.DATABASE_PORT,
                                     host=Config.DATABASE_HOST,
                                     password=Config.DATABASE_PASSWORD
                                     )
        self.cursor = self.conn.cursor()
        return self.cursor

    def stopDataBaseConnection(self):
        """commit and stop connection to postgres sql"""
        self.conn.commit()
        self.conn.close()
        self.cursor.close()
