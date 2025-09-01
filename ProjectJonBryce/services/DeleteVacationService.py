import asyncio
from srcs.dal_b.Vacation_dao import Vacation_dao
from srcs.dal_b.Like_dao import Like_dao


def deleteVacation(id_vacation: int):
    """delete some vacation"""
    vacation_dao = Vacation_dao()
    b = False
    for vacation in vacation_dao.getAll():
        if vacation.id == id_vacation:
            b = True
    if not b:
        raise Exception('bad vacation id')
    vacation_dao.deleteVacationById(id_vacation)
    print('vacation deleted')
    
    like_dao = Like_dao()
    likes = like_dao.getAll()
    for like in likes:
        if like.id_vacation == id_vacation:
            like_dao.deleteLikeByLike(like)
            print('like deleted')
