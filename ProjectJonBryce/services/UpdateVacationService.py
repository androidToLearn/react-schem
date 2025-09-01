import asyncio
from srcs.dal_b.Vacation_dao import Vacation_dao
from modules1.Vacation import Vacation


def updateVacation(vacation_id: int, id_country: int, description: str, date_start: str, date_end: str, price: int, filename: str, isInOther: bool):
    """inside this function i try to update vacation , if not good date - sign i insert reverse date therefore i do the function more time with 'isInOther' = True and reverse the date properly ,in addition i add necessary zeros to relevant date """
    b = False
    try:
        int(date_start[0:4])
        int(date_end[0:4])
    except Exception:
        # רק אם הפורמאט לא הפוך תוסיף את ה0
        # אני הופך את הפורמאט תמיד שהיום יהיה ראשון לכן תמיד
        # b = True

        b = True

    if b:
        date_start = addZeros(date_start, isRevers=isInOther)
        date_end = addZeros(date_end, isRevers=isInOther)
    # גם אם אני מוסיף 0 בכל מיני מקומות האחרון לא יעבוד
    try:
        price = int(price)
    except Exception as e:
        raise Exception('fill all fields')

    if len(str(id_country)) > 0 and len(description) > 0 and len(date_start) > 0 and len(date_end) > 0 and len(str(price)) > 0:
        if price < 0 or price > 10000:
            raise Exception("bad price")
        else:
            if isBigger(date_start, date_end, isInOther) or (len(date_start) != 10 or len(date_end) != 10):
                raise Exception("bad date!")
            else:
                if isInOther:
                    v = Vacation(vacation_id, id_country, description,
                                 date_start[::-1], date_end[::-1], int(price), filename)
                else:
                    v = Vacation(vacation_id, id_country, description,
                                 date_start, date_end, int(price), filename)
                vacation_dao = Vacation_dao()
                vacation_dao.updateVacationById(v)
                print('vacation updated')
    else:
        raise Exception("fill all fields")


def isBigger(date_start: str, date_end: str, isInOther: bool):
    """check if date_start bigger then date_end and return True or False. if 'isInOther' - reverse date enter to 'updateVacations' i do reverse again after get the day month or year"""
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
