import asyncio
from modules1.Vacation import Vacation
from srcs.dal_b.Vacation_dao import Vacation_dao


def getAllVacations():
    """get all vacations from sql without filtering and by order of small date to big date"""

    keepVacation = Vacation(-1, 1, "", "", "", 1, "")
    vacation_dao = Vacation_dao()
    allVacations = vacation_dao.getAll()
    b = True
    while b:
        b = False
        for i in range(0, len(allVacations) - 1):
            if isBiggerDate(allVacations[i], allVacations[i + 1]):
                v1 = allVacations[i]
                v2 = allVacations[i + 1]
                b = True
                keepVacation.id = v1.id
                keepVacation.id_country = v1.id_country
                keepVacation.description = v1.description
                keepVacation.date_start = v1.date_start
                keepVacation.date_end = v1.date_end
                keepVacation.price = v1.price
                keepVacation.image_name = v1.image_name

                v1.id = v2.id
                v1.id_country = v2.id_country
                v1.description = v2.description
                v1.date_start = v2.date_start
                v1.date_end = v2.date_end
                v1.price = v2.price
                v1.image_name = v2.image_name

                v2.id = keepVacation.id
                v2.id_country = keepVacation.id_country
                v2.description = keepVacation.description
                v2.date_start = keepVacation.date_start
                v2.date_end = keepVacation.date_end
                v2.price = keepVacation.price
                v2.image_name = keepVacation.image_name
    return allVacations


def changeOrder(date: str):
    """replace reverse date that start with year to start with the day"""
    """for example 2026/10/10 -> 10.10.2026"""
    return date[8:10] + '.' + date[5:7] + '.' + date[0:4]


def isBiggerDate(v1: str, v2: str):
    """get date from v1 and v2 string and check if v1 has older or closer start_date then v2"""
    try:
        day = int(v1.date_start[0:2])
        month = int(v1.date_start[3:5])
        year = int(v1.date_start[6:10])
    except Exception as e:
        date_start = changeOrder(v1.date_start)
        day = int(date_start[0:2])
        month = int(date_start[3:5])
        year = int(date_start[6:10])
    try:
        day2 = int(v2.date_start[0:2])
        month2 = int(v2.date_start[3:5])
        year2 = int(v2.date_start[6:10])
    except Exception as e:
        date_start = changeOrder(v2.date_start)
        day2 = int(date_start[0:2])
        month2 = int(date_start[3:5])
        year2 = int(date_start[6:10])

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
