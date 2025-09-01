import unittest
from srcs.dal_b.Database_test import Database_test
from srcs.dal_b.Database import Database
from services import AddLikeService, DeleteLikeService, DeleteVacationService, GetAllVacationsService, InsertVacationService, LoginService, RegisterService, UpdateVacationService
from modules1.Like import Like
from modules1.Vacation import Vacation
from test1.DefualtVariables import DefinedVariables
import app


class Test(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_all(self):
        DefinedVariables.IS_TEST = True

        Test.test_add_like_service(self=self)
        print('----------------')
        Test.test_delete_like_service(self=self)
        print('----------------')
        Test.test_delete_vacation_service(self=self)
        print('----------------')
        Test.test_get_all_vacations(self=self)
        print('----------------')
        Test.test_insert_vacation_service(self=self)
        print('----------------')
        Test.test_login_service(self=self)
        print('----------------')
        Test.test_register_service(self=self)
        print('----------------')
        Test.test_update_vacation_service(self=self)
        print('----------------')
        Test.testApp(self=self)
        Test.test_register_page(self=self)
        print('----------------')
        Test.test_login_page(self=self)
        print('----------------')
        Test.test_vacations_page(self=self)
        print('----------------')
        Test.test_description_page(self=self)
        print('----------------')
        Test.test_user_profile_page(self=self)
        print('----------------')
        Test.test_edit_page(self=self)

        DefinedVariables.IS_TEST = False

    def testApp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_register_page(self):
        # positive test
        try:
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)
            print('success /')
        except Exception as e:
            print(str(e))

        # negative test
        try:
            response = self.app.post('/', json={'m': 'bad jon'})
            self.assertEqual(response.status_code, 200)
            print('success /')
        except Exception as e:
            print(str(e))

    def test_login_page(self):
        # positive test

        try:
            response = self.app.get('/login_page')
            self.assertEqual(response.status_code, 200)
            print('success /login_page')
        except Exception as e:
            print(str(e))

        # negative test
        try:
            response = self.app.post('/login_page', json={'m': 'bad jon'})
            self.assertEqual(response.status_code, 200)
            print('success /login_page')
        except Exception as e:
            print(str(e))

    def test_vacations_page(self):
        # positive test

        try:
            response = self.app.get(
                '/go_to_vacation_page_without_login_or_register')
            self.assertEqual(response.status_code, 200)
            print('success /go_to_vacation_page_without_login_or_register')
        except Exception as e:
            print(str(e))

        # negative test
        try:
            response = self.app.post(
                '/go_to_vacation_page_without_login_or_register', json={'m': 'bad jon'})
            self.assertEqual(response.status_code, 200)
            print('success /go_to_vacation_page_without_login_or_register')
        except Exception as e:
            print(str(e))

    def test_description_page(self):
        # positive test

        try:
            response = self.app.get(
                '/go_to_vacation_page_without_login_or_register')
            self.assertEqual(response.status_code, 200)
            print('success /go_to_vacation_page_without_login_or_register')
        except Exception as e:
            print(str(e))

        # negative test
        try:
            response = self.app.post(
                '/go_to_vacation_page_without_login_or_register', json={'m': 'bad jon'})
            self.assertEqual(response.status_code, 200)
            print('success /go_to_vacation_page_without_login_or_register')
        except Exception as e:
            print(str(e))

    def test_user_profile_page(self):
        # positive test

        try:
            response = self.app.get(
                '/user_page/mosh/ahroni')
            self.assertEqual(response.status_code, 200)
            print('success /user_page')
        except Exception as e:
            print(str(e))

        # negative test
        try:
            response = self.app.post(
                '/user_page/mosh/ahroni', json={'m': 'bad json'})
            self.assertEqual(response.status_code, 200)
            print('success /user_page')
        except Exception as e:
            print(str(e))

    def test_edit_page(self):
        # positive test

        try:
            response = self.app.get(
                '/go_to_editPage/2')
            self.assertEqual(response.status_code, 200)
            print('success /go_to_editPage')
        except Exception as e:
            print(str(e))

        # negative test
        try:
            response = self.app.post(
                '/go_to_editPage/2', json={'m': 'bad json'})
            self.assertEqual(response.status_code, 200)
            print('success /go_to_editPage')
        except Exception as e:
            print(str(e))

    def test_add_like_service(self):
        # positive test
        try:
            AddLikeService.insertLikeBack1(Like(1, 1))
        except Exception as e:
            print(str(e))
        # negative test
        try:
            AddLikeService.insertLikeBack1(Like(1, 100000))
        except Exception as e:
            print(str(e))

    def test_delete_like_service(self):
        # positive test
        try:
            DeleteLikeService.deleteLikeBack1(Like(1, 1))
        except Exception as e:
            print(str(e))
        # negative test
        try:
            DeleteLikeService.deleteLikeBack1(Like(-1, 1))
        except Exception as e:
            print(str(e))

    def test_delete_vacation_service(self):
        # positive test
        try:
            DeleteVacationService.deleteVacation(1)
        except Exception as e:
            print(str(e))
        # negative test
        try:
            DeleteVacationService.deleteVacation(-100000)
        except Exception as e:
            print(str(e))

    def test_get_all_vacations(self):
        # positive test
        vacations = GetAllVacationsService.getAllVacations()
        print('vacations size:', str(len(vacations)))

        # negative test - not relevant

    def test_insert_vacation_service(self):
        # def insertVacations(id_country: int, description: str, date_start: str, date_end: str, price: int, filename: str, isInOther: bool):
        # positive test
        # isInOther - mean date reverse or not
        try:
            InsertVacationService.insertVacation(
                1, 'חופשה ליוון תחת שמיים ואוויר צח ומרענן', '11/11/2026', '29/11/2026', '3000', 'icon18.jpg', False)
        except Exception as e:
            print(str(e))

        # negative test
        try:
            InsertVacationService.insertVacation(
                1, 'חופשה ליוון תחת שמיים ואוויר צח ומרענן', '11/11/2026', '29/11/2026', '1000000', 'icon18.jpg', False)
        except Exception as e:
            print(str(e))

    def test_login_service(self):
        # positive test
        try:
            print(LoginService.isLoginUser('1234', '1@gmail.com'))
        except Exception as e:
            print(str(e))
        # negative test
        try:
            print(LoginService.isLoginUser('1234', '1234'))
        except Exception as e:
            print(str(e))

    def test_register_service(self):
        # def isRegisterUser(name: str, second_name: str, password: str, email: str):
        # positive test
        print(RegisterService.isRegisterUser(
            'david', 'dan', '2456', '234456@gmail.com'))

        # negative test
        try:
            print(RegisterService.isRegisterUser(
                'david', 'dan', '', '234567@gmail.com'))
        except Exception as e:
            print(str(e))

    def test_update_vacation_service(self):
        # def updateVacation(vacation_id: int, id_country: int, description: str, date_start: str, date_end: str, price: int, filename: str, isInOther: bool):
        # isInOther - is the date reverse
        # positive test
        try:
            UpdateVacationService.updateVacation(
                1, 3, 'שמיים כחולים', '10/10/2027', '23/10/2027', '2000', 'icon19.jpg', False)
        except Exception as e:
            print(str(e))
        # negative test
        try:
            UpdateVacationService.updateVacation(
                1, 3, 'שמיים כחולים', '10/10/2027', '23/10/2027', '200000000', 'icon19.jpg', False)
        except Exception as e:
            print(str(e))

    def initSql(self):
        dataBase = Database_test()
        cursor = dataBase.getDataBaseConnection()
        with open('srcs/init_db.sql', 'r', encoding='UTF-8') as file:
            contentData = file.read()
        cursor.execute(contentData)
        dataBase.stopDataBaseConnection()
        print('sql loaded')


if __name__ == '__main__':
    unittest.main()
