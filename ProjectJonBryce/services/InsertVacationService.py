import asyncio
from datetime import datetime
from srcs.dal_b.Vacation_dao import Vacation_dao
from modules1.Vacation import Vacation


def insertVacation(id_country: int, description: str, date_start: str, date_end: str, price: int, filename: str, isInOther: bool):
    """inside this function i try to insert vacation , if not good date - sign i insert reverse date therefore i do the function more time with 'isInOther' = True and reverse the date properly ,in addition i add necessary zeros to relevant date """

   
    b = False
    try:
        int(date_start[0:4])
        int(date_end[0:4])
    except Exception:
        # רק אם הפורמאט לא הפוך תוסיף את ה0
        b = True

    if b:
        date_start = addZeros(date_start, isRevers=isInOther)
        date_end = addZeros(date_end, isRevers=isInOther)
    try:
        price = int(price)
    except Exception as e:
        raise Exception("fill all fields")
    if len(str(id_country)) > 0 and len(description) > 0 and len(date_start) > 0 and len(date_end) > 0 and len(str(price)) > 0:
        if price < 0 or price > 10000:
            raise Exception("bad price")
        else:
            if isBigger(date_start, date_end, isInOther) or (len(date_start) != 10 or len(date_end) != 10):
                raise Exception("bad date!")
            else:
                now = datetime.now().strftime("%d/%m/%Y")

                if isBigger(now, date_start, isInOther) or isBigger(now, date_end, isInOther):
                    raise Exception("bad start date")
                vacation_dao = Vacation_dao()
                if isInOther:
                    vacation_dao.insertVacation(
                        Vacation(-1, id_country, description, date_start[::-1], date_end[::-1], int(price), filename))
                else:
                    vacation_dao.insertVacation(
                        Vacation(-1, id_country, description, date_start, date_end, int(price), filename))
                print('vacation inserted')

    else:
        raise Exception("fill all fields")


def addZeros(date: str, isRevers: bool):
    """add zeros to 'date' according the order of the date and 'isRevers' if the days or years first"""
    if isRevers:
        try:
            int(date[0:2])
            isWithZero = True
        except Exception:
            isWithZero = False
        if not isWithZero:
            date = date[0:1] + '0' + date[1:]

        try:
            int(date[3:5])
            isWithZero = True
        except Exception:
            isWithZero = False
        if not isWithZero:
            date = date[0:4] + '0' + date[4:]
    else:
        try:
            int(date[0:2])
            isWithZero = True
        except Exception:
            isWithZero = False
        if not isWithZero:
            date = '0' + date[0:]

        try:
            int(date[3:5])
            isWithZero = True
        except Exception:
            isWithZero = False
        if not isWithZero:
            date = date[0:3] + '0' + date[3:]
    return date


def isBigger(date_start: str, date_end: str, isInOther: str):
    """check if 'date_start' bigger then 'date_end' and if 'isInOther' the date enter to 'insertVacations' as [::-1] and here for example  [0:2] and again [::-1] """
    if isInOther:
        try:
            day = int(date_start[0:2][::-1])
            month = int(date_start[3:5][::-1])
            year = int(date_start[6:10][::-1])

            day2 = int(date_end[0:2][::-1])
            month2 = int(date_end[3:5][::-1])
            year2 = int(date_end[6:10][::-1])
        except Exception:
            return True
    else:
        day = int(date_start[0:2])
        month = int(date_start[3:5])
        year = int(date_start[6:10])

        day2 = int(date_end[0:2])
        month2 = int(date_end[3:5])
        year2 = int(date_end[6:10])

    if year > year2:
        return True
    elif year < year2:
        return False

    if month > month2:
        return True
    elif month < month2:
        return False

    if day > day2:
        return True

    elif day < day2:
        return False
    return False
