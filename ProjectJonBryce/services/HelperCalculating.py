from datetime import datetime
from modules1 import Vacation


def getDataAboutVacations(allVacations):

    allVacations = doSameDateForAllVacations(allVacations)
    numBefore = 0
    numCurrent = 0
    numFuture = 0
    for v in allVacations:
        date_str = v.date_start
        dateStart = datetime.strptime(date_str, "%d/%m/%Y").date()
        date_str = v.date_end
        dateEnd = datetime.strptime(date_str, "%d/%m/%Y").date()
        dateNow = datetime.now()
        if dateNow < dateStart:
            numBefore += 1
        elif dateNow >= dateStart and dateNow <= dateEnd:
            numCurrent += 1
        else:
            numFuture += 1
    return {"pastVacations": numBefore, "ongoingVacations": numCurrent, "futureVacations": numFuture}


def doSameDateForAllVacations(allVacations):
    allV = []
    for v in allVacations:
        allV.append(Vacation(id=v.id, id_country=v.id_country, description=v.description,  price=v.price,
                    image_name=v.image_name, date_start=getGoodDate(v.date_start), date_end=getGoodDate(v.date_end)))
    return allV


def getGoodDate(date):
    try:
        int(date[0:4])
        return date[8:10] + date[5:7] + date[0:4]
    except Exception as e:
        return date
