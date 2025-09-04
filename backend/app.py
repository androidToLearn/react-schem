from flask import Flask, render_template, jsonify, request
import requests
from flask_cors import CORS
import uuid
from flask import Flask, redirect, url_for, render_template, request, jsonify, send_from_directory, Response

from srcs.dal_b.Like_dao import Like_dao
from srcs.dal_b.Country_dao import Country_dao
import json
from modules1.User import User
from modules1.Like import Like
import os
from srcs.dal_b.Database import Database
from werkzeug.utils import secure_filename
from modules1.Country import Country
from modules1.Vacation import Vacation
from srcs.dal_b.Vacation_dao import Vacation_dao
import os
from srcs.dal_b.User_dao import User_dao
import service.HelperCalculating as HelperCalculating
from srcs.dal_b.Database import Database


app = Flask(__name__)


@app.route("/")
def serve():
    return send_from_directory("dist", 'index.html')


@app.route("/assets/<path:filename>")
def serveassets(filename):
    return send_from_directory("dist/assets", filename)


@app.route('/api/login', methods=['POST'])
def doLogin():
    """רישום משתמש למערכת לפי שם וסיסמה ואם admin"""
    userPost = request.get_json()

    allUsers = User_dao().getAll()
    print(userPost['name'] + userPost['password'])
    for user in allUsers:
        print('name:', user.name, 'password:', user.password)
        if user.name == userPost['name'] and user.password == userPost['password'] and user.id_role == 0:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                BASE_DIR, 'data', f'oneUser{str(uuid.getnode())}.json')

            myUserJson = {'user': user.name, 'password': user.password}
            with open(file_path, 'w') as file:
                json.dump(myUserJson, file, indent=4)
                return jsonify({'message': 'logined!'})
        elif user.name == userPost['name'] and user.password == userPost['password']:
            return jsonify({'message': 'user not admin'})

    return jsonify({'message': 'user not found'})


@app.route('/api/hasLogined', methods=['GET'])
def hasLogined():
    """מחזיר אם המשתמש מחובר למערכת"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# נתיב מוחלט לקובץ
    file_path = os.path.join(
        BASE_DIR, 'data', f'oneUser{str(uuid.getnode())}.json')

    return jsonify({'isLogined': os.path.exists(file_path)})


@app.route('/api/vacations/stats', methods=['GET'])
def getDataAboutVacations():
    """מחזיר את הנתונים כמה חופשות בעבר בהווה ובעתיד"""
    allVacations = Vacation_dao().getAll()
    return jsonify(HelperCalculating.getDataAboutVacations(allVacations))


@app.route('/api/users/total', methods=['GET'])
def getNumUsers():
    """מחזיר total users במערכת"""
    numUsers = len(User_dao().getAll())
    return jsonify({'totalUsers': numUsers})


@app.route('/api/likes/total', methods=['GET'])
def getLikesTotal():
    """מחזיר total likes במערכת"""
    numLikes = len(Like_dao().getAll())
    return jsonify({'totalLikes': numLikes})


@app.route('/api/likes/distribution', methods=['GET'])
def getNumLikesForEveryCountry():
    """מחזיר כמות לייקים שיש לכל מדינה"""
    likes = Like_dao().getAll()
    dictCountryWithLike = {}
    arrayFormatOfTheDict = []

    for l in likes:
        vacation = getVacationById(l.id_vacation)
        country = getNameCountryById(vacation.id_country)
        if country in dictCountryWithLike.keys():
            dictCountryWithLike[country] += 1
        else:
            dictCountryWithLike[country] = 1

    for key in dictCountryWithLike.keys():
        arrayFormatOfTheDict.append({key: dictCountryWithLike[key]})
    return arrayFormatOfTheDict


def getVacationById(idVacation: int):
    """מחזיר vacation לפי id"""
    vacations = Vacation_dao().getAll()
    for v in vacations:
        if v.id == idVacation:
            return v
    return None


def getNameCountryById(idCountry):
    """מחזיר את המדינה לפי id"""
    countries = Country_dao().getAll()
    for c in countries:
        if c.id == idCountry:
            return c.name_country
    return None


@app.route('/api/sumCountries', methods=['GET'])
def getSumCountries():
    """מחזיר את מספר המדינות במערכת"""
    countries = Country_dao().getAll()
    return jsonify({'sumCountries': len(countries)})


@app.route('/api/futureLikes', methods=['POST', 'GET'])
def getFutureLikes():
    """avg time to new vacation - avg likes for every vacation - future likes according date"""
    nextTime = request.get_json()
    days = 0
    if not nextTime['years'] == -1:
        days = nextTime['years'] * 365
    if not nextTime['month'] == -1:
        days += nextTime['month'] * 30
    if not nextTime['days'] == -1:
        days += nextTime['days']

    # הזמן שעבר אם יש זמן בין רישום חופשה אחת לשנייה
    avgTimeToNewVacation = HelperCalculating.getAvgTimeToNewVacation()
    print('avgTimeToNewVacation', avgTimeToNewVacation)

    timeFirstVacation = HelperCalculating.getTimeToFirstVacation(
        avgTimeToNewVacation)
    print('timeFirstVacation', timeFirstVacation)

    avgLikeToEveryVacation = HelperCalculating.getAvgLikeForEveryVacation()
    print('avgLikeToEveryVacation', avgLikeToEveryVacation)
    countVacations = 0
    if days >= timeFirstVacation:
        days -= timeFirstVacation
        countVacations += 1
    if avgTimeToNewVacation != 0:

        while days >= avgTimeToNewVacation:
            days -= avgTimeToNewVacation
            countVacations += 1

    numFutureLikes = avgLikeToEveryVacation * countVacations

    return jsonify({'futureVacations': countVacations, 'futureLikes': numFutureLikes})


@app.route('/api/logout', methods=['GET'])
def logout():
    """יציאה מהמערכת - מוחק את הjson של המשתמש"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# נתיב מוחלט לקובץ
    file_path = os.path.join(
        BASE_DIR, 'data', f'oneUser{str(uuid.getnode())}.json')
    if os.path.exists(file_path):
        os.remove(file_path)
    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
