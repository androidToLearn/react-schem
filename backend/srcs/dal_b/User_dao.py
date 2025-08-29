from srcs.dal_b.Database import Database
from modules1.User import User
from srcs.dal_b.Database_test import Database_test
from test1.DefualtVariables import DefinedVariables as main



class User_dao:
    COLUMN_ID = "id"
    COLUMN_NAME = "name"
    COLUMN_SECOND_NAME = "second_name"
    COLUMN_PASSWORD = "password"
    COLUMN_EMAIL = "email"
    COLUMN_ID_ROLE = "id_role"
    TABLE_NAME = "users111"

    def __init__(self):
        """constractor / בנאי"""
        pass

    def insertUser(self, user: User):
        """insert users to sql"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute(f"""INSERT INTO {User_dao.TABLE_NAME} ({User_dao.COLUMN_NAME}, {User_dao.COLUMN_SECOND_NAME}, 
                                                            {User_dao.COLUMN_PASSWORD}, {User_dao.COLUMN_EMAIL}, {User_dao.COLUMN_ID_ROLE}) 
                            VALUES (%s, %s, %s, %s, %s) RETURNING {User_dao.COLUMN_ID}""",
                       (user.name, user.second_name, user.password, user.email, user.id_role))

        user.id = cursor.fetchone()[0]
        dataBase.stopDataBaseConnection()

    def getAll(self):
        """get all users"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute("SELECT * FROM " + User_dao.TABLE_NAME)
        users = cursor.fetchall()

        allUsers = []
        if not users:
            return allUsers

        for user in users:
            allUsers.append(
                User(user[0], user[1], user[2], user[3], user[4], user[5]))
        dataBase.stopDataBaseConnection()
        return allUsers

    def deleteUserById(self, id: int):
        """delete some user by id"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute(
            f"""DELETE FROM {User_dao.TABLE_NAME} WHERE {User_dao.COLUMN_ID} = {id}""")
        dataBase.stopDataBaseConnection()

    # def __init__(self, id: int, name: str, second_name: str, password: str, email: str, id_role: int):

    def getUserById(self, id: int):
        """get user by id"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute(
            f"""SELECT * FROM {User_dao.TABLE_NAME} WHERE {User_dao.COLUMN_ID} = {id}""")
        result = cursor.fetchone()
        dataBase.stopDataBaseConnection()
        return User(id, result[1], result[2], result[3], result[4], result[5])

    def updateUserById(self, user: User):
        """update user by id"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute(f"""UPDATE {User_dao.TABLE_NAME} 
                        SET {User_dao.COLUMN_NAME} = '{user.name}', 
                            {User_dao.COLUMN_SECOND_NAME} = '{user.second_name}', 
                            {User_dao.COLUMN_PASSWORD} = '{user.password}', 
                            {User_dao.COLUMN_EMAIL} = '{user.email}', 
                            {User_dao.COLUMN_ID_ROLE} = {user.id_role} 
                        WHERE {User_dao.COLUMN_ID} = {user.id}""")
        dataBase.stopDataBaseConnection()

    def deleteAll(self):
        """delete all users"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        deleteTable = "DROP TABLE IF EXISTS " + User_dao.TABLE_NAME
        createTable = f"""CREATE TABLE IF NOT EXISTS {User_dao.TABLE_NAME} ({User_dao.COLUMN_ID} SERIAL INTEGER KEY,
        {User_dao.COLUMN_NAME} VARCHAR(225),
        {User_dao.COLUMN_SECOND_NAME} VARCHAR(225),
        {User_dao.COLUMN_PASSWORD} VARCHAR(225),
        {User_dao.COLUMN_EMAIL} VARCHAR(225),
        {User_dao.COLUMN_ID_ROLE} INTEGER
        )"""
        cursor.execute(deleteTable)
        cursor.execute(createTable)

        dataBase.stopDataBaseConnection()
