from srcs.dal_b import User_dao
from modules1 import User
from srcs.dal_b import Like_dao


def addUser(user):
    user_dao = User_dao()
    if user.id_role == User.ID_ADMIN:
        raise Exception("can't enter admin user!")
    else:
        user_dao.insertUser(user)


def getUserByEmailAndPassword(email, password):
    user_dao = User_dao()
    users = user_dao.getAll()
    for user in users:
        if user.password == password and user.email == email:
            return user
    return None


def isEmailExists(email):
    user_dao = User_dao()
    users = user_dao.getAll()
    for user in users:
        if user.email == email:
            return True
    return False


def addLike(like):
    like_dao = Like_dao()
    like_dao.insertLike(like)


def removeLike(like):
    like_dao = Like_dao()
    like_dao.deleteLikeByLike()
