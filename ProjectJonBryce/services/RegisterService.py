import asyncio
from srcs.dal_b.User_dao import User_dao
from modules1.User import User


def isRegisterUser(name: str, second_name: str, password: str, email: str):
    """"enter to the system in register page with good new user according the criteria and return the relevant user"""
    if len(name.strip()) > 0 and len(second_name.strip()) > 0 and len(password.strip()) > 0 and len(email.strip()) > 0:
        if '@gmail.com' in email or '@gov.co.il' in email:
            if len(password) >= 4:

                user_dao = User_dao()
                users = user_dao.getAll()

                if not isGmailAppear(users, email):
                    user = User(-1, name, second_name, password, email, 1)
                    user_dao.insertUser(user)
                    return user
                else:
                    raise Exception("failed , gmail appear , try again!")
            else:
                raise Exception("password must be with less four length")
        else:
            raise Exception("email pattern wrong")
    else:
        raise Exception("fill all fields")


def isGmailAppear(users: list[User], email: str):
    """check if one user in 'users' list has email like 'email' and return true or false"""
    for user in users:
        if user.email == email:
            return True
    return False
