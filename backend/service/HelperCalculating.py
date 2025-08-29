from datetime import datetime
from modules1.Vacation import Vacation
from srcs.dal_b.Like_dao import Like_dao
from srcs.dal_b.Vacation_dao import Vacation_dao
from modules1.Vacation import Vacation
from typing import List


def getDataAboutVacations(allVacations: List[Vacation]):
    """מחזיר את החופשות שהיו פעם עכשיו ובעתיד"""

    allVacations = doSameDateForAllVacations(allVacations)
    numBefore = 0
    numCurrent = 0
    numFuture = 0
    dateNow = datetime.now().date()
    for v in allVacations:
        date_start = v.date_start
        dateStart = datetime.strptime(date_start,  '%d%m%Y').date()
        date_end = v.date_end
        dateEnd = datetime.strptime(date_end,  '%d%m%Y').date()

        if dateNow < dateStart:
            numBefore += 1
        elif dateNow >= dateStart and dateNow <= dateEnd:
            numCurrent += 1
        else:
            numFuture += 1
    return {"pastVacations": numBefore, "ongoingVacations": numCurrent, "futureVacations": numFuture}


def doSameDateForAllVacations(allVacations: List[Vacation]):
    """מחזיר את כל החופשות עם אותו פורמאט תאריך התחלה וסוף"""
    allV = []
    for v in allVacations:
        allV.append(Vacation(id=v.id, id_country=v.id_country, description=v.description,  price=v.price,
                    image_name=v.image_name, date_start=getGoodDate(v.date_start), date_end=getGoodDate(v.date_end)))
    return allV


def getGoodDate(date: str):
    """מחזיר את התאריך בפורמאט מהימים לשנים"""
    try:
        int(date[0:4])
        return date[8:10] + date[5:7] + date[0:4]
    except Exception as e:
        return date[0:2] + date[3:5] + date[6:10]


def getAvgTimeToNewVacation():
    """מחזיר את הממוצע כל כמה זמן מתווספת חופשה למערכת"""
    allVacations = doSameDateForAllVacations(Vacation_dao().getAll())
    dates = convertVacationToDateStart(allVacations)

    isChanged = True
    keepDate = -1

    while isChanged:
        isChanged = False
        for i in range(len(dates) - 1):
            oneDate = dates[i]
            oneDate = datetime.strptime(oneDate,  '%d%m%Y').date()
            secondDate = dates[i + 1]
            secondDate = datetime.strptime(secondDate,  '%d%m%Y').date()
            if secondDate < oneDate:
                keepDate = dates[i]
                dates[i] = dates[i + 1]
                dates[i + 1] = keepDate
                isChanged = True
    sumDaysBetweenDates = 0
    for i in range(len(dates) - 1):
        sumDaysBetweenDates += subAsDays(dates[i + 1], dates[i])
    timeNoVacation = getTimeNoVacation()
    if (sumDaysBetweenDates / len(dates)) - timeNoVacation < 0:
        # הרבה זמן לא היה חופשה - אולי אפילו המערכת מושבתת
        sumDaysBetweenDates += timeNoVacation

    return sumDaysBetweenDates / len(dates)


def subAsDays(oneDate: str, secondDate: str):
    """מחזיר את הפרש הימים בין התאריכים"""
    oneDate = datetime.strptime(oneDate,  '%d%m%Y').date()
    secondDate = datetime.strptime(secondDate,  '%d%m%Y').date()
    return (oneDate - secondDate).days


def convertVacationToDateStart(allVacations: List[Vacation]):
    """מחזיר רשמיה רק של התאריכים ההתחלתיים של החופשות"""
    dates = []
    for vacation in allVacations:
        dates.append(vacation.date_start)
    return dates


def getTimeToFirstVacation(avgTimeNextVacation: int):
    """עוד כמה זמן החופשה הבאה שתהיה במערכת - לפי ממוצע פחות כמה זמן שכבר עבר"""
    timeNoVacation = getTimeNoVacation()
    if avgTimeNextVacation - timeNoVacation < 0:
        return avgTimeNextVacation

    return (avgTimeNextVacation - timeNoVacation)


def getTimeNoVacation():
    """מחזיר כמה זמן לא היתווספה חופשה"""
    allVacations = doSameDateForAllVacations(Vacation_dao().getAll())
    dates = convertVacationToDateStart(allVacations)
    biggestDate = datetime.strptime(dates[0],  '%d%m%Y').date()
    for i in range(len(dates)):
        oneDate = dates[i]
        oneDate = datetime.strptime(oneDate,  '%d%m%Y').date()
        if biggestDate < oneDate:
            biggestDate = oneDate

    dateNow = datetime.now().date()
    print('biggestDate', str((dateNow - biggestDate).days))
    if (dateNow - biggestDate).days < 0:
        # החופשה עוד לא הגיע
        return 0
    return (dateNow - biggestDate).days


def getAvgLikeForEveryVacation():
    """מחזיר ממוצע לייקים עבור כל חופשה"""
    likes = Like_dao().getAll()
    vacations = Vacation_dao().getAll()
    return len(likes) / len(vacations)
