import asyncio
from srcs.dal_b.User_dao import User_dao
from modules1.User import User


def isLoginUser(password: str, email: str):
    """enter to the system in login page with good email and password and return the relevant user"""
    if len(password.strip()) > 0 and len(email.strip()) > 0:

        if '@gmail.com' in email or '@gov.co.il' in email:
            if len(password) >= 4:
                user_dao = User_dao()
                users = user_dao.getAll()
                user = isExistsUser(users, password, email)
                if user != None:
                    return user
                else:
                    raise Exception(
                        "failed , gmail or password wrong , try again!")
            else:
                raise Exception("password must be with less four length")
        else:
            raise Exception("email wrong")
    else:
        raise Exception("fill all fields")


def isExistsUser(users: list[User], password: str, email: str):
    """check if is user exists in the list 'users' and return it"""
    for user in users:
        if user.email == email and user.password == password:
            return user
    return None
