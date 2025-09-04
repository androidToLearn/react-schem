import uuid
from flask import Flask, redirect, url_for, render_template, request, jsonify, send_from_directory, Response
from services import GetAllVacationsService
from services import RegisterService
from services import LoginService
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
from services import DeleteVacationService
from services import InsertVacationService
from services import UpdateVacationService
from srcs.dal_b.User_dao import User_dao
import services.HelperCalculating as HelperCalculating


app = Flask(__name__)


UPLOAD_FILE = os.path.join(os.getcwd(), 'uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FILE


@app.route('/get_image/<string:image_name>', methods=['GET'])
def get_image(image_name: str):
    """return some image with name 'image_name' from uploads images"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], image_name)


@app.route('/upload_image/<string:vacation_id>', methods=['POST'])
def upload_image(vacation_id: str):
    """upload image and return json
"""
    filename = ''
    if 'file' in request.files:
        print('file found')
        file = request.files['file']
        if file.filename != '':
            print('good name file')
            if isGoodName(file.filename):
                filename = file.filename
                print('good best', file.filename)
                if not os.path.exists(UPLOAD_FILE):
                    os.mkdir(UPLOAD_FILE)
                # filename = secure_filename(file.filename)
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))

    country = request.form.get('country')
    description = request.form.get('description')
    date_start = request.form.get('date_start')
    date_end = request.form.get('date_end')
    price = request.form.get('price')

    country_dao = Country_dao()
    idCountry = getCountry(country, country_dao.getAll())

    if int(vacation_id) == -1:
        print('inside inserting')

        try:
            print('inside inserting')
            print('filename before inserting', file.filename)
            InsertVacationService.insertVacation(
                idCountry, description, date_start, date_end, price, filename, False)
        except Exception as e:
            # try:
            # למקרה שהתאריך כולו הפוך
            try:
                InsertVacationService.insertVacation(
                    idCountry, description, date_start[::-1], date_end[::-1], price, filename, True)
            except Exception as e:
                return jsonify({'message': str(e)})
    else:
        print('inside update')

        try:
            print('inside update')
            if filename == '':
                filename = Vacation_dao().getVacationById(vacation_id).image_name
            UpdateVacationService.updateVacation(
                int(vacation_id), idCountry, description, date_start, date_end, price, filename, False)
        except Exception as e:
            try:
                UpdateVacationService.updateVacation(
                    int(vacation_id), idCountry, description, date_start[::-1], date_end[::-1], price, filename, True)
            except Exception as e:
                return jsonify({'message:': str(e)})

    return redirect(url_for('in_like_page'))


@app.route('/user_page/<string:name>/<string:second_name>')
def user_page(name, second_name):
    try:
        data_dir = os.path.join(os.getcwd(), 'data')
        file_path = os.path.join(
            data_dir, 'user' + str(get_mac_address()) + '.json')
        with open(file_path, 'r') as file:
            myUserToInsertFiles = json.load(file)

        my_user = User(myUserToInsertFiles['m'][0], myUserToInsertFiles['m'][1], myUserToInsertFiles['m'][2],
                       myUserToInsertFiles['m'][3], myUserToInsertFiles['m'][4], myUserToInsertFiles['m'][5])
    except Exception as e:
        # no user and no login or register therefore I can put default user with as user value = 1
        #    def __init__(self, id: int, name: str, second_name: str, password: str, email: str, id_role: int):
        my_user = User(-1, 'undefined', 'undefined', '', '', 1)

    try:
        with open(os.path.join(os.getcwd(), 'data', 'isReOrLo' + str(get_mac_address()) + '.json'), 'r') as file:
            islr = json.load(file)['islr']
    except Exception as e:
        # המשתמש לא מחובר
        islr = True

    return render_template('userPage.html', name=name, second_name=second_name, my_user=my_user, islr=islr)


def getCountry(nameC: str, countries: list[Country]):
    """return the id of country with name 'nameC' if no those country in sql insert new country with the same to sql and return the id"""
    for c in countries:
        if c.name_country == nameC:
            return c.id

    country_dao = Country_dao()
    country = Country(-1, nameC)
    country_dao.insertCountry(country)
    return country.id


def isGoodName(filename: str):
    """return True or False if file name is image"""
    a = ['jpg', 'png', 'jpeg', 'webp', 'svg']
    return '.' in filename and filename.split('.', 1)[1] in a


@app.route('/')
def index():
    """go to enter page / register page"""

    try:
        with open(os.path.join(os.getcwd(), 'data', 'isReOrLo' + str(get_mac_address()) + '.json'), 'r') as file:
            islr = json.load(file)['islr']
    except Exception as e:
        # המשתמש לא מחובר
        islr = True

    try:
        data_dir = os.path.join(os.getcwd(), 'data')
        file_path = os.path.join(
            data_dir, 'user' + str(get_mac_address()) + '.json')
        with open(file_path, 'r') as file:
            myUserToInsertFiles = json.load(file)

        my_user = User(myUserToInsertFiles['m'][0], myUserToInsertFiles['m'][1], myUserToInsertFiles['m'][2],
                       myUserToInsertFiles['m'][3], myUserToInsertFiles['m'][4], myUserToInsertFiles['m'][5])
    except Exception as e:
        # no user and no login or register therefore I can put default user with as user value = 1
        #    def __init__(self, id: int, name: str, second_name: str, password: str, email: str, id_role: int):
        my_user = User(-1, 'undefined', 'undefined', '', '', 1)
    return render_template('enterPage.html', islr=islr, my_user=my_user)


# from javascript update page for like
@app.route('/likes_page', methods=['POST', 'GET'])
def likesPage():
    """add like to sql with id user and id vacation"""
    json = request.get_json()
    like = Like(int(json['id_user']), int(json['id_vacation']))
    likeDao = Like_dao()
    try:
        likeDao.insertLike(like=like)
        return jsonify({})
    except Exception as e:
        return jsonify({})


@app.route('/likes_page_delete', methods=['POST', 'GET'])
def likesPageDelete():
    # delete like from sql with id user and id vacation
    json = request.get_json()
    like = Like(int(json['id_user']), int(json['id_vacation']))
    likeDao = Like_dao()
    try:
        likeDao.deleteLikeByLike(like=like)
        return jsonify({})
    except Exception as e:
        return jsonify({})

    # update to sql

# move here from page1


@app.route('/in_like_page', methods=['POST', 'GET'])
def in_like_page():
    """this function treat in registering or login or search vacation or return from add or update vacation and return appropriate json - if 'message' : 'go' - go to vacations page in java script / node.js ,in addition insert to json the relevant content about vacations"""
    try:
        allContent = request.get_json()
    except Exception as e:
        allContent = {}
    try:
        name = allContent['name']
        second_name = allContent['second_name']

    except Exception as e:
        print('not register')

    try:
        password = allContent['password']
        gmail = allContent['email']
    except Exception as e:
        print('not login only search or add vacation')
    if 'name' in allContent.keys():
        # sometimes i come from search or add vacation vacation without register or login therefore i check if its from login or register page
        # here in register page
        try:
            message = RegisterService.isRegisterUser(
                name=name, second_name=second_name, password=password, email=str(gmail))
        except Exception as e:
            return jsonify({'message': str(e)})

        myUserToInsertFiles = {'m': [message.id, message.name, message.second_name,
                                     message.password, message.email, message.id_role]}
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        file_path = os.path.join(
            data_dir, 'user' + str(get_mac_address()) + '.json')
        with open(file_path, 'w') as file:
            json.dump(myUserToInsertFiles, file, indent=4)
    elif 'password' in allContent.keys():
        # here in login page
        try:
            message = LoginService.isLoginUser(
                password=password, email=str(gmail))
        except Exception as e:
            return jsonify({'message':  str(e)})
        # editing dto json in order to refresh page page2.html properly with the current user
        myUserToInsertFiles = {'m': [message.id, message.name, message.second_name,
                                     message.password, message.email, message.id_role]}
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        file_path = os.path.join(
            data_dir, 'user' + str(get_mac_address()) + '.json')
        with open(file_path, 'w') as file:
            json.dump(myUserToInsertFiles, file, indent=4)

        # WHEN simple updating page(not entering like back from add vacation)
    else:
        try:
            # get from json as object user...
            data_dir = os.path.join(os.getcwd(), 'data')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            file_path = os.path.join(
                data_dir, 'user' + str(get_mac_address()) + '.json')
            with open(file_path, 'r') as file:
                myUserToInsertFiles = json.load(file)

            message = User(myUserToInsertFiles['m'][0], myUserToInsertFiles['m'][1], myUserToInsertFiles['m'][2],
                           myUserToInsertFiles['m'][3], myUserToInsertFiles['m'][4], myUserToInsertFiles['m'][5])
        except Exception as e:
            myUserToInsertFiles = {'m': [-1, 'undefined', '', '', '', 1]}
            message = User(-1, 'undefined', '', '', '', 1)
    vacationAll = []
    my_is_like = []

    with open(os.path.join(os.getcwd(), 'data', 'file2' + str(get_mac_address()) + '.json'), 'r') as file:
        searchJson = json.load(file)
    for vacation in GetAllVacationsService.getAllVacations():
        vacationAll.append({'id': vacation.id, 'num_likes': getNumLikeByIdVacation(vacation.id), 'country': findCountryName(
            vacation.id_country), 'description': vacation.description, 'date_start': vacation.date_start, 'date_end': vacation.date_end, 'price': vacation.price, 'image_name': vacation.image_name})
        my_is_like.append(isHasLike(message.id, vacation.id))

    bVacations = []
    b_my_is_like = []

    try:
        (bVacations, b_my_is_like) = accordingSearchJson(
            vacationAll, my_is_like, searchJson)
    except Exception as e:
        return jsonify({'message': 'bad arguments'})

    with open(os.path.join(os.getcwd(), 'data', 'file2_data_all' + str(get_mac_address()) + '.json'), 'w') as file:
        json.dump({'vacations': bVacations, 'myIsLikes': b_my_is_like,
                  'my_user': myUserToInsertFiles}, file, indent=4)

    return jsonify({'message': 'go'})


@app.route('/go_to_page2', methods=['GET'])
def go_to_page2():
    """go to vacations page with the good date from json"""
    with open(os.path.join(os.getcwd(), 'data', 'file2_data_all' + str(get_mac_address()) + '.json'), 'r') as file:
        content = json.load(file)

    content['my_user'] = User(content['my_user']['m'][0], content['my_user']['m'][1], content['my_user']['m'][2],
                              content['my_user']['m'][3], content['my_user']['m'][4], content['my_user']['m'][5])

    with open(os.path.join(os.getcwd(), 'data', 'isReOrLo' + str(get_mac_address()) + '.json'), 'w') as file:
        json.dump({'islr': False}, file, indent=4)

    return render_template('vacationPage.html', vacations=content['vacations'], myIsLikes=content['myIsLikes'], my_user=content['my_user'], islr=False, isHasPermissionToEdit=True)


@app.route('/go_to_vacation_page_without_login_or_register')
def go_to_vacation_page_without_login_or_register():
    """go_to_vacation_page_without_login_or_register after go"""
    with open(os.path.join(os.getcwd(), 'data', 'file2_data_all' + str(get_mac_address()) + '.json'), 'r') as file:
        content = json.load(file)

    content['my_user'] = User(content['my_user']['m'][0], content['my_user']['m'][1], content['my_user']['m'][2],
                              content['my_user']['m'][3], content['my_user']['m'][4], content['my_user']['m'][5])

    return render_template('vacationPage.html', vacations=content['vacations'], myIsLikes=content['myIsLikes'], my_user=content['my_user'], islr=True, isHasPermissionToEdit=False)


@app.route('/do_out')
def out_system():

    myUserToInsertFiles = {'m': [-1, 'undefined', 'undefined',
                                     '', '', 1]}
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    file_path = os.path.join(
        data_dir, 'user' + str(get_mac_address()) + '.json')
    with open(file_path, 'w') as file:
        json.dump(myUserToInsertFiles, file, indent=4)

    with open(os.path.join(os.getcwd(), 'data', 'isReOrLo' + str(get_mac_address()) + '.json'), 'w') as file:
        json.dump({'islr': json.dumps(True)}, file, indent=4)
    return redirect(url_for('index'))


@app.route('/login_page', methods=['GET'])
def login_page():
    # go to login page
    try:
        with open(os.path.join(os.getcwd(), 'data', 'isReOrLo' + str(get_mac_address()) + '.json'), 'r') as file:
            islr = json.load(file)['islr']
    except Exception as e:
        # המשתמש לא מחובר
        islr = True
    try:
        data_dir = os.path.join(os.getcwd(), 'data')
        file_path = os.path.join(
            data_dir, 'user' + str(get_mac_address()) + '.json')
        with open(file_path, 'r') as file:
            myUserToInsertFiles = json.load(file)

        my_user = User(myUserToInsertFiles['m'][0], myUserToInsertFiles['m'][1], myUserToInsertFiles['m'][2],
                       myUserToInsertFiles['m'][3], myUserToInsertFiles['m'][4], myUserToInsertFiles['m'][5])
    except Exception as e:
        # no user and no login or register therefore I can put default user with as user value = 1
        #    def __init__(self, id: int, name: str, second_name: str, password: str, email: str, id_role: int):
        my_user = User(-1, 'undefined', 'undefined', '', '', 1)
    return render_template('login_page.html', islr=islr, my_user=my_user)


def get_mac_address():
    """return the unique address of this Device """
    mac = uuid.getnode()
    return mac


def getNumLikeByIdVacation(id: int):
    """return the num of like of of vacation by id vacation"""
    like_dao = Like_dao()
    return len(like_dao.getAllByIdVacation(id))


def accordingSearchJson(vacations: list[Vacation], my_is_like: list[bool], searchJson: dict):
    """filter the vacations according the search widget"""
    new_vac = []
    newMyIsLike = []

    i = 0
    for v in vacations:
        try:
            if ((searchJson['id'] == '-1' or searchJson['id'] == v['id']) and
                (searchJson['country'] == '-1' or str(searchJson['country']).lower() == str(
                    v['country']).lower()) and
                (searchJson['description'] == '-1' or str(searchJson['description']).lower() in str(v['description']).lower()) and
                (searchJson['price'] == '-1' or int(searchJson['price']) >= v['price']) and
                ((searchJson['ischeaked'] ==
                    '-1' or searchJson['ischeaked'] == str(3)) or (my_is_like[i] and searchJson['ischeaked'] == str(1)) or (not my_is_like[i] and searchJson['ischeaked'] == str(2)))
                    and (searchJson['month_start'] == '-1' or isInSameMonth(searchJson['month_start'], v['date_start']))
                    and (searchJson['year_start'] == '-1' or isSameYear(searchJson['year_start'], v['date_start']))
                    and (searchJson['days_vacation'] == '-1' or isSameTimeVacation(searchJson['days_vacation'], v['date_start'], v['date_end']))):

                v['date_start'] = v['date_start'].replace('-', '.')
                v['date_end'] = v['date_end'].replace('-', '.')
                v['date_end'] = changeOrder(v['date_end'])
                v['date_start'] = changeOrder(v['date_start'])

                new_vac.append(v)
                newMyIsLike.append(my_is_like[i])
            i += 1
        except Exception as e:
            if ((searchJson['id'] == '-1' or searchJson['id'] == v['id']) and
                (searchJson['country'] == '-1' or str(searchJson['country']).lower() == str(
                    v['country']).lower()) and
                (searchJson['description'] == '-1' or str(searchJson['description']).lower() in str(v['description']).lower()) and
                (searchJson['price'] == '-1' or int(searchJson['price']) >= v['price']) and
                ((searchJson['ischeaked'] ==
                    '-1' or searchJson['ischeaked'] == str(3)) or (my_is_like[i] and searchJson['ischeaked'] == str(1)) or (not my_is_like[i] and searchJson['ischeaked'] == str(2)))
                    and (searchJson['month_start'] == '-1' or isInSameMonthReverse(searchJson['month_start'], v['date_start'][::-1]))
                    and (searchJson['year_start'] == '-1' or isInSameYearReverse(searchJson['year_start'], v['date_start'][::-1]))
                    and (searchJson['days_vacation'] == '-1' or isSameTimeVacationReverse(searchJson['days_vacation'], v['date_start'][::-1], v['date_end'][::-1]))):

                v['date_start'] = v['date_start'].replace('-', '.')

                v['date_end'] = v['date_end'].replace('-', '.')
                v['date_end'] = changeOrder(v['date_end'])
                v['date_start'] = changeOrder(v['date_start'])

                new_vac.append(v)
                newMyIsLike.append(my_is_like[i])
            i += 1

    return (new_vac, newMyIsLike)


def changeOrder(date: str):
    """the function change the order of the date to be in order of day to year"""
    string = ''
    try:
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
    except Exception as e:
        print('-------', date)
        day = int(date[0:2])
        month = int(date[3:5])
        year = int(date[6:10])

    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)

    string = str(day) + '.' + str(month) + '.' + str(year)
    return string


def isInSameMonthReverse(month_start_in_json: str, date_start: str):
    """when the 'date_start' reverse check if month of 'date_start' equal to 'month_start_in_json' (parse both two to int)"""
    m = int(date_start[3:5][::-1])
    return int(month_start_in_json) == m


def isInSameYearReverse(year_start_in_json: str, date_start: str):
    """when the 'date_start' reverse check if year of 'date_start' equal to 'year_start_in_json' (parse both two to int)"""

    y = int(date_start[6:10][::-1])
    return int(year_start_in_json) == y


def isSameYear(year_start_in_json: str, date_start: str):
    """when the 'date_start' not reverse check if year of 'date_start' equal to 'year_start_in_json' (parse both two to int)"""

    y = int(date_start[6:10])
    return int(year_start_in_json) == y


def isInSameMonth(month_start_in_json, date_start):
    """when the 'date_start' not reverse check if year of 'date_start' equal to 'year_start_in_json' (parse both two to int)"""

    m = int(date_start[3:5])
    return int(month_start_in_json) == m


def isSameTimeVacation(stringDays: str, date_start: str, date_end: str):
    """check if the num days of some vacation equals to 'stringDays' as int"""
    s_day = int(date_start[0:2])
    s_month = int(date_start[3:5])
    s_year = int(date_start[6:10])

    day = int(date_end[0:2])
    month = int(date_end[3:5])
    year = int(date_end[6:10])

    numDays = 0
    numDays += (year - s_year) * 365
    numDays += (month - s_month) * 30
    numDays += day - s_day + 1  # pluse 1 - if same day is one day.
    return numDays == int(stringDays)


def isSameTimeVacationReverse(stringDays: str, date_start: str, date_end: str):
    """when the 'date_start' and 'date_end' reverse check if the num days of some vacation according 'date_start' and 'date_end' equals to 'stringDays' as int"""

    s_day = int(date_start[0:2][::-1])
    s_month = int(date_start[3:5][::-1])
    s_year = int(date_start[6:10][::-1])

    day = int(date_end[0:2][::-1])
    month = int(date_end[3:5][::-1])
    year = int(date_end[6:10][::-1])

    numDays = 0
    numDays += (year - s_year) * 365
    numDays += (month - s_month) * 30
    numDays += day - s_day + 1  # pluse 1 - if same day is one day.
    return numDays == int(stringDays)


def findCountryName(countryId: int):
    """return the name of some country in sql with the same id like 'countryId'"""
    country_dao = Country_dao()
    for country in country_dao.getAll():
        if country.id == countryId:
            return country.name_country
    return None


def isHasLike(userId: int, vacationId: int):
    """when I enter to vacations page I want to see if I do like on vacation already in this function I check if I did like on some vacation according my 'userId' and 'vacationId'"""
    like_dao = Like_dao()
    for like in like_dao.getAll():

        if like.id_user == userId and vacationId == like.id_vacation:
            return True
    return False


@app.route('/go_to_editPage/<string:vacation_id>', methods=['GET'])
def goToAddOrUpdateVacation(vacation_id: int):
    """go to edit page with the relevant data"""
    vacation_dao = Vacation_dao()
    countries = Country_dao()
    vacation = vacation_dao.getVacationById(vacation_id)
    countries1 = countries.getAll()
    countriesJson = []

    try:
        with open(os.path.join(os.getcwd(), 'data', 'isReOrLo' + str(get_mac_address()) + '.json'), 'r') as file:
            islr = json.load(file)['islr']
    except Exception as e:
        # המשתמש לא מחובר
        islr = True

    try:
        data_dir = os.path.join(os.getcwd(), 'data')
        file_path = os.path.join(
            data_dir, 'user' + str(get_mac_address()) + '.json')
        with open(file_path, 'r') as file:
            myUserToInsertFiles = json.load(file)

        my_user = User(myUserToInsertFiles['m'][0], myUserToInsertFiles['m'][1], myUserToInsertFiles['m'][2],
                       myUserToInsertFiles['m'][3], myUserToInsertFiles['m'][4], myUserToInsertFiles['m'][5])
    except Exception as e:
        # no user and no login or register therefore I can put default user with as user value = 1
        #    def __init__(self, id: int, name: str, second_name: str, password: str, email: str, id_role: int):
        my_user = User(-1, 'undefined', 'undefined', '', '', 1)
    for c in countries1:
        countriesJson.append(c.todict())

    try:
        countryName = findCountryName(vacation.id_country)
        vacation.date_start = changeOrder(vacation.date_start)
        vacation.date_end = changeOrder(vacation.date_end)
        vacation.date_end = vacation.date_end.replace('.', '-')
        vacation.date_start = vacation.date_start.replace('.', '-')
        return render_template('editPage.html', vacation=vacation, country_name=countryName, vacation_id=vacation_id, countries=countries.getAll(), countriesJson=json.dumps(countriesJson), islr=islr, my_user=my_user)
    except Exception:
        return render_template('editPage.html', vacation=None, country_name=None, vacation_id=vacation_id, countries=countries.getAll(), countriesJson=json.dumps(countriesJson), islr=islr, my_user=my_user)


@app.route('/go_to_description_page/<string:description>/<string:image_name>/<string:title>', methods=['GET'])
def go_to_description_page(description, image_name, title):
    """go to description page"""

    try:
        with open(os.path.join(os.getcwd(), 'data', 'isReOrLo' + str(get_mac_address()) + '.json'), 'r') as file:
            islr = json.load(file)['islr']

    except Exception as e:
        # המשתמש לא מחובר
        islr = True

    try:
        data_dir = os.path.join(os.getcwd(), 'data')
        file_path = os.path.join(
            data_dir, 'user' + str(get_mac_address()) + '.json')
        with open(file_path, 'r') as file:
            myUserToInsertFiles = json.load(file)

        my_user = User(myUserToInsertFiles['m'][0], myUserToInsertFiles['m'][1], myUserToInsertFiles['m'][2],
                       myUserToInsertFiles['m'][3], myUserToInsertFiles['m'][4], myUserToInsertFiles['m'][5])
    except Exception as e:
        # no user and no login or register therefore I can put default user with as user value = 1
        #    def __init__(self, id: int, name: str, second_name: str, password: str, email: str, id_role: int):
        my_user = User(-1, 'undefined', 'undefined', '', '', 1)
    return render_template('page_description.html', description=description, image_name=image_name, title=title, islr=islr, my_user=my_user)


@app.route('/delete_vacation/<int:id>')
def deleteVacation(id: int):
    """delete vacation by id"""
    DeleteVacationService.deleteVacation(id)
    return redirect(url_for('in_like_page'))


@app.route('/send_search_json', methods=['POST'])
def send_search_json():
    """insert to file2 the json of search"""
    myjson = request.get_json()
    dir_path = os.path.join(os.getcwd(), 'data')
    print("Directory exists:", os.path.exists(dir_path))

    os.makedirs(os.path.join(os.getcwd(), 'data'), exist_ok=True)
    with open(os.path.join(os.getcwd(), 'data', 'file2' + str(get_mac_address()) + '.json'), 'w') as file:
        json.dump(myjson, file, indent=4)

    return redirect(url_for('in_like_page'))


@app.route('/get_search_json')
def get_json():
    """get the search json from file2"""
    with open(os.path.join(os.getcwd(), 'data', 'file2' + str(get_mac_address()) + '.json'), 'r') as file:
        searchJson = json.load(file)
    return searchJson


@app.route('/vacations/stats')
def getDataAboutVacations():
    allVacations = Vacation_dao().getAll()
    return jsonify(HelperCalculating.getDataAboutVacations(allVacations))


@app.route('/users/total')
def getNumUsers():
    numUsers = len(User_dao().getAll())
    return jsonify({'totalUsers': numUsers})


@app.route('/likes/total')
def getLikesTotal():
    numLikes = len(Like_dao().getAll())
    return jsonify({'totalLikes': numLikes})


@app.route('/likes/distribution')
def getNumLikesForEveryCountry():
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


def getVacationById(idVacation):
    vacations = Vacation_dao().getAll()
    for v in vacations:
        if v.id == idVacation:
            return v
    return None


def getNameCountryById(idCountry):
    countries = Country_dao().getAll()
    for c in countries:
        if c.id == idCountry:
            return c.name_country
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=True)
