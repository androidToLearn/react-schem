from srcs.dal_b.Database import Database
import modules1.Role as Role
from srcs.dal_b.Database_test import Database_test
from test1.DefualtVariables import DefinedVariables as main



class Role_dao:
    """every user have role - 0 : admin , 1 : simple user , there is two roles"""
    COLUMN_ID = "id"
    COLUMN_NAME = "name"
    TABLE_NAME = "roles"

    def __init__(self):
        """בנאי / constractor"""
        pass

    def insertRole(self, role: Role):
        """change name of some role"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute(
            f"""INSERT INTO {Role_dao.TABLE_NAME} ({Role_dao.COLUMN_NAME}) VALUES (%s) RETURNING {role.id}""", (role.type_name,))
        role.id = cursor.fetchone()[0]
        dataBase.stopDataBaseConnection()

    def deleteRoleById(self, id: int):
        """delete role by id"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute(
            f"""DELETE FROM {Role_dao.TABLE_NAME} WHERE {Role_dao.COLUMN_ID} = {id}""")
        dataBase.stopDataBaseConnection()

    def updateRoleById(self, role: Role):
        """update some role by id"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute(
            f"""UPDATE {Role_dao.TABLE_NAME} SET {Role_dao.COLUMN_NAME} = {role.type_name} WHERE {Role_dao.COLUMN_ID} = {role.id}""")
        dataBase.stopDataBaseConnection()

    def getRoleById(self, id: int):
        """get role by id"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute("SELECT * FROM " +
                       Role_dao.TABLE_NAME + "WHERE = " + id)
        result = cursor.fetchone()
        dataBase.stopDataBaseConnection()
        return Role(result[0], result[1])

    def getAll(self):
        """get all roles"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        cursor.execute("SELECT * FROM " + Role_dao.TABLE_NAME)
        results = cursor.fetchall()
        dataBase.stopDataBaseConnection()
        allRoles = []
        for result in results:
            allRoles.append(Role(result[0], result[1]))
        return allRoles

    def deleteAll(self):
        """delete all roles"""
        if main.IS_TEST:
            dataBase = Database_test()
        else:
            dataBase = Database()
        cursor = dataBase.getDataBaseConnection()
        deleteTable = "DROP TABLE IF EXISTS " + Role_dao.TABLE_NAME
        createTable = f"""CREATE TABLE IF NOT EXISTS {Role_dao.TABLE_NAME} ({Role_dao.COLUMN_ID} SERIAL PRIMARY KEY,
        {Role_dao.COLUMN_NAME} VARCHAR(225))"""
        cursor.execute(deleteTable)
        cursor.execute(createTable)

        dataBase.stopDataBaseConnection()
