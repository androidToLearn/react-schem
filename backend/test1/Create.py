import unittest
from srcs.dal_b.Database_test import Database_test
from srcs.dal_b.Database import Database


class Create(unittest.TestCase):
    """מחלקה לאיתחול הsql"""

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def initSql(self):
        """איתחול הsql"""
        dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        with open('srcs/init_db.sql', 'r', encoding='UTF-8') as file:
            contentData = file.read()
        cursor.execute(contentData)
        dataBase.stopDataBaseConnection()
        print('sql loaded')


if __name__ == '__main__':
    unittest.main()
