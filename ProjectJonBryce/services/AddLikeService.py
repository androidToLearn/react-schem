import asyncio
from srcs.dal_b.Like_dao import Like_dao
from srcs.dal_b.User_dao import User_dao
from srcs.dal_b.Vacation_dao import Vacation_dao
from modules1.Like import Like
from modules1.Vacation import Vacation

#    def __init__(self, id: int, name: str, second_name: str, password: str, email: str, id_role: int):


def insertLikeBack1(like: Like):
    """insert new like to some user with some vacation"""
    vacation_dao = Vacation_dao()
    user_dao = User_dao()
    vacations = vacation_dao.getAll()
    users = user_dao.getAll()
    if not isIdAppear(like.id_vacation, vacations):
        raise Exception("bad vacation id!")
    if not isIdAppear(like.id_user, users):
        raise Exception("bad user id")
    like_dao = Like_dao()
    like_dao.insertLike(like)
    print('like inserted')


def isIdAppear(id: int, objects: list[Vacation]):
    """check if id is appear in the objects"""
    for o in objects:
        if o.id == id:
            return True
    return False
