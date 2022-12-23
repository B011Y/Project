import sqlite3
connection = sqlite3.connect('final.db')
sql = connection.cursor()

def checking(user_id):
    """
    Проверка есть ли пользователь в базе данных

    :param user_id: айди пользователя
    :return: True or False
    """

    connection = sqlite3.connect('final.db')
    sql = connection.cursor()

    sql.execute(f'SELECT us_id FROM users WHERE us_id = {user_id};')

    if not sql.fetchall():
        return True
    else:
       return False

def registration(user_id,user_name,user_number):
    """
    Занесение данных регистрации в таблицу

    :param user_id: айди пользователя
    :param user_name: имя пользователя
    :param user_number: номер телефона пользователя
    :return:
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'INSERT INTO users (us_id, us_name, us_number) VALUES ({user_id}, "{user_name}", "{user_number}");')
    connection.commit()

def get_hotels():
    """
    Выбор всех отелей с таблицы

    :return:
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute('SELECT h_name FROM hotels;')

    return sql.fetchall()

def show_hotel(name):
    """
    Вывод описания

    :param name: название отеля
    :return: описание отеля
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'SELECT h_description,h_photo,h_rating FROM hotels WHERE h_name = "{name}" ;')

    return sql.fetchall()

def free_rooms(h_name):
    """
    Показ свободных комнат

    :param h_name: название отеля
    :return: комнаты, которые свободный
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'SELECT rooms FROM {h_name} Where position = "свободно";')

    return sql.fetchall()

def busy_rooms(h_name):
    """
    Показ занятых комнат

    :param h_name: название отеля
    :return: комнаты, которые заняты
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'SELECT rooms FROM {h_name} Where position = "занято";')

    return sql.fetchall()



def show_room(r_name,hotel):
    """
    Выводит описание выбранной комнаты
    :param r_name: название комнаты
    :param hotel: определённый отель
    :return: описание комнаты
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'SELECT r_description,r_price,r_photo FROM {hotel} WHERE rooms = "{r_name}" ;')

    return sql.fetchall()



def add_to_cart(user_id, number, hotel):
    """
    Добавление в личную карточку

    :param user_id: айди пользователя
    :param number: номер комнаты
    :param hotel: определённый отель
    :return:
    """

    connection = sqlite3.connect('final.db')
    sql = connection.cursor()

    sql.execute(f'INSERT INTO user_cart (user_id, room, hotel) VALUES ({user_id}, "{number}", "{hotel}");')

    connection.commit()

def show_cart(user_id):
    """
    Показ на личной карточки пользователя

    :param user_id: айди пользователя
    :return: вывод карточки
    """

    connection = sqlite3.connect('final.db')
    sql = connection.cursor()

    sql.execute(f'SELECT room,hotel FROM user_cart WHERE user_id={user_id};')
    return sql.fetchall()

def qwerty(hotel,room):
    """
    Показ значения

    :param hotel: опрделённый отель
    :param room: выбраная комната
    :return: положение комнаты
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()

    sql.execute(f'SELECT r_condition FROM {hotel} WHERE rooms = "{room}";')
    return sql.fetchall()


def qwerty_update(hotel,room):
    """
    Смена положения со 'свободного' на 'ожидает обратки'
    :param hotel: определённый отель
    :param room: выбранная комната
    :return:
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'UPDATE {hotel} SET r_condition = "ожидает обратки" WHERE rooms = "{room}";')

    connection.commit()

def checking2(user_id,hotel):
    """
    Проверка есть ли отзыв именно опр. отеля пользоателем

    :param user_id: айди пользователя
    :param hotel: определённый отель
    :return: True or False
    """

    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'SELECT user_id,hotel FROM reviews WHERE user_id = {user_id} AND hotel = "{hotel}";')
    if not sql.fetchall():
        return True
    else:
        return False

def review(user_id,hotel,stars,review):
    """
    Занесение в таблицу оценк и отзыва

    :param user_id: айди пльзователя
    :param hotel: определённый отель
    :param stars: оценка пользоателя
    :param review: отзыв пользователя
    :return:
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'INSERT INTO reviews (user_id, hotel, stars,review) VALUES ({user_id}, "{hotel}", {stars}, "{review}");')
    connection.commit()

def review_update(user_id,hotel,stars,review):
    """
    Изменение в таблице оценки и отзыва

    :param user_id: айди пльзователя
    :param hotel: определённый отель
    :param stars: оценка пользоателя
    :param review: отзыв пользователя
    :return:
    """

    connection = sqlite3.connect('final.db')
    sql = connection.cursor()

    sql.execute(f'UPDATE reviews SET hotel= "{hotel}",stars = {stars},review= "{review}" WHERE user_id = {user_id};')
    connection.commit()

def rating(hotel):
    """
    Показ среднего рейтинга отеля

    :param hotel: определённый отель
    :return: оценки отеля
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'SELECT stars FROM reviews WHERE hotel="{hotel}";')
    return sql.fetchall()

def average_rating(hotel,y):
    """
    Обновление рейтинга

    :param hotel: определённый отель
    :param y: рейтинг отеля
    :return:
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()

    sql.execute(f'UPDATE hotels SET h_rating = {y} WHERE h_name = "{hotel}";')
    connection.commit()

def sort_rate():
    """
    Сортировка по рейтингу

    :return:
    """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'SELECT h_name FROM hotels ORDER BY h_rating ASC;')
    return sql.fetchall()

def sort_pay():
    """
   Сортировка по средней стоймости

   :return:
   """
    connection = sqlite3.connect('final.db')
    sql = connection.cursor()
    sql.execute(f'SELECT h_name FROM hotels ORDER BY h_apay ASC;')
    return sql.fetchall()










