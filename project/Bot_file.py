import telebot
from telebot import types
import main

#подключение
bot = telebot.TeleBot('5438364844:AAGtQcfdfmHw-bMcQgE9tRPBgxFYRz7METk')
admin = 352719257


#обработка команды start
@bot.message_handler(commands=['start'])
def start(message):
    """
    Обрабатывает команду старта бота

    :param message:
    :return:
    """
    if main.checking(message.from_user.id):
        bot.send_message(message.from_user.id, 'привет, введи своё имя')
        bot.register_next_step_handler(message, get_name)
    else:
        kb = types.ReplyKeyboardMarkup(True, True)
        item1 = "Отели"
        item2 = "Информация"
        kb.add(item1,item2)


        bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=kb)

def get_name(message):
    """
    Получение имени клиента

    :param message: сообщение
    :return:
    """
    username = message.text

    bot.send_message(message.from_user.id, 'введите номер:')
    bot.register_next_step_handler(message, get_number, username)

def get_number(message, username):
    """
    Получение номера клиента

    :param message:
    :param username:
    :return:
    """
    user_number = message.text
    main.registration(message.from_user.id, username, user_number)

    kb = types.ReplyKeyboardMarkup(True, True)
    item1 = "Отели"
    item2 = "Информация"
    kb.add(item1, item2)


    bot.send_message(message.from_user.id, 'Вы успешно зарегистрировались!', reply_markup=kb)
    bot.send_message(message.from_user.id, 'выберите категорию')
    bot.register_next_step_handler(message, text)

@bot.message_handler(content_types=['text'])
def text(message):
    """
    Обрабатывет основной код

    :param message: сообщение
    :return:
    """

    if message.text == "Отели":
        kb2 = types.ReplyKeyboardMarkup(True, True)

        kb2.add("назад")
        kb2.add("Сортировка")
        for i in main.get_hotels():
            kb2.add(i[0])

        bot.send_message(message.from_user.id,"Выберите отель",reply_markup=kb2)
        bot.register_next_step_handler(message,hotel_selection)

    if message.text == "Информация":
        kb3 = types.ReplyKeyboardMarkup(True, True)

        item1 = "назад"
        item2 = "Подтвердить бронь"
        item3 = "Отменить бронь"
        kb3.add(item1,item2,item3)
        full_message = 'Информация\n\n'
        for i in main.show_cart(message.from_user.id):
            full_message += f'Отель: {i[1]} Комната: {i[0]}\n'

        bot.send_message(message.from_user.id,full_message,reply_markup=kb3)


def hotel_selection(message):
    """
    Выбор отеля

    :param message: сообщение
    :return:
    """
    if message.text == "назад":
        kb = types.ReplyKeyboardMarkup(True, True)
        item1 = "Отели"
        item2 = "Информация"
        kb.add(item1, item2)

        bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=kb)
    if message.text == "Сортировка":
        kb2 = types.ReplyKeyboardMarkup(True, True)
        item3 = "по рейтенгу(от меньшего к большему)"
        item4 = "по средней стоемости(от меньшего к большему)"
        kb2.add(item3,item4)
        bot.send_message(message.from_user.id,"Выберите сортировку", reply_markup=kb2)
        bot.register_next_step_handler(message,sort)

    if message.text != "назад" and message.text != "Сортировка":

        hotel = message.text
        full_info = main.show_hotel(hotel)[0]
        kb3 = types.ReplyKeyboardMarkup(True, True)

        item1 = "Назад"
        item2 = "На главное меню"
        item3 = "Свободные номера"
        item4 = "Занятые номера"
        item5 = "Отзывы"
        kb3.add(item1,item2,item3,item4,item5)

        bot.send_photo(message.from_user.id, photo=full_info[1], caption=f'описание: {full_info[0]}\n\n рейтинг: {full_info[-1]} ',reply_markup=kb3)
        bot.send_message(message.from_user.id, "Выберите категорию")
        bot.register_next_step_handler(message,rooms_selection,hotel)

def sort(message):
    """
    Cортировка отелей

    :param message: сообщение
    :return:
    """
    if message.text == "по рейтенгу(от меньшего к большему)":
        kb1 = types.ReplyKeyboardMarkup(True, True)
        kb1.add("назад")
        kb1.add("Сортировка")
        for i in main.sort_rate():
            kb1.add(i[0])

        bot.send_message(message.from_user.id, "Выберите отель", reply_markup=kb1)
        bot.register_next_step_handler(message, hotel_selection)
    if message.text == "по средней стоемости(от меньшего к большему)":
        kb2 = types.ReplyKeyboardMarkup(True, True)
        kb2.add("назад")
        kb2.add("Сортировка")
        print(main.sort_pay())
        for i in main.sort_pay():
            kb2.add(i[0])

        bot.send_message(message.from_user.id, "Выберите отель", reply_markup=kb2)
        bot.register_next_step_handler(message, hotel_selection)


def rooms_selection(message,hotel):
    """

    Выбор категорий свободных и не свободных комнат

    :param message: сообщение
    :param hotel: определённый отель
    :return:
    """
    if message.text == "Назад":
        kb2 = types.ReplyKeyboardMarkup(True, True)

        kb2.add("назад")
        kb2.add("Сортировка")
        for i in main.get_hotels():
            kb2.add(i[0])

        bot.send_message(message.from_user.id, "Выберите отель", reply_markup=kb2)
        bot.register_next_step_handler(message, hotel_selection)
    if message.text == "На главное меню":
        kb = types.ReplyKeyboardMarkup(True, True)
        item1 = "Отели"
        item2 = "Информация"
        kb.add(item1, item2)

        bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=kb)

    if message.text == "Свободные номера":
        kb4 = types.ReplyKeyboardMarkup(True, True)
        kb4.add("назад")
        for i in main.free_rooms(hotel):
            kb4.add(i[0])

        bot.send_message(message.from_user.id, "Выберите комнату",reply_markup=kb4)
        bot.register_next_step_handler(message,room,hotel)
    if message.text == "Занятые номера":

        kb5 = types.ReplyKeyboardMarkup(True, True)
        kb5.add("назад")
        for i in main.busy_rooms(hotel):
            kb5.add(i[0])

        bot.send_message(message.from_user.id, "Выберите комнату", reply_markup=kb5)
        bot.register_next_step_handler(message,room,hotel)
    if message.text == "Отзывы":

        if main.checking2(message.from_user.id,hotel):
            kb6 = types.ReplyKeyboardMarkup(True, True)
            item3 = "назад"
            item4 = "Написать отзыв"
            kb6.add(item3,item4)
            bot.send_message(message.from_user.id,"Выберите действие",reply_markup=kb6)
            bot.register_next_step_handler(message,write_review,hotel)
        else:
            kb7 = types.ReplyKeyboardMarkup(True,True)
            item5 = "назад"
            item6 = "Изменить отзыв"
            kb7.add(item5,item6)
            bot.send_message(message.from_user.id,"Выберите действие",reply_markup=kb7)
            bot.register_next_step_handler(message, update_review, hotel)

def write_review(message,hotel):
    """
    Обработка отзыва

    :param message: сообщение
    :param hotel: определённый отель
    :return:
    """
    if message.text == "назад":
        kb3 = types.ReplyKeyboardMarkup(True, True)

        item1 = "Назад"
        item2 = "На главное меню"
        item3 = "Свободные номера"
        item4 = "Занятые номера"
        item5 = "Отзывы"
        kb3.add(item1, item2, item3, item4, item5)
        bot.send_message(message.from_user.id, "Выберите категорию",reply_markup=kb3)
        bot.register_next_step_handler(message, rooms_selection, hotel)
    if message.text == "Написать отзыв":
        kb1 = types.ReplyKeyboardMarkup(True, True)
        item5 = "назад"
        kb1.add(item5,"1","2","3","4","5")
        bot.send_message(message.from_user.id,"Выберите оценку",reply_markup=kb1)
        bot.register_next_step_handler(message,get_stars,hotel)


def get_stars(message,hotel):
    """
    получение оценки от клиента

    :param message: сообщение
    :param hotel: определённый отель
    :return:
    """
    stars = message.text

    bot.send_message(message.from_user.id, 'Напишите отзыв')
    bot.register_next_step_handler(message, get_review, hotel, stars)

def get_review(message,hotel,stars):
    """
    Получение отзыва от клиента и вычисление общего рейтинга

    :param message: сообщение
    :param hotel: определённый отель
    :param stars: оценка полученная от пользователя
    :return:
    """
    review = message.text
    main.review(message.from_user.id,hotel,stars,review)
    x = []
    for i in main.rating(hotel):
        x.append(i[0])
    y = sum(x) / len(x)
    main.average_rating(hotel,y)
    kb3 = types.ReplyKeyboardMarkup(True, True)

    item1 = "Назад"
    item2 = "На главное меню"
    item3 = "Свободные номера"
    item4 = "Занятые номера"
    item5 = "Отзывы"
    kb3.add(item1, item2, item3, item4, item5)

    bot.send_message(message.from_user.id, "Ваш комментарий учтён",reply_markup=kb3)
    bot.register_next_step_handler(message, rooms_selection, hotel)


def update_review(message, hotel):
    """
    Обрабатывание измененя отзыва пользователя

    :param message:сообщение
    :param hotel: определённый отель
    :return:
    """
    if message.text == "назад":
        kb3 = types.ReplyKeyboardMarkup(True, True)

        item1 = "Назад"
        item2 = "На главное меню"
        item3 = "Свободные номера"
        item4 = "Занятые номера"
        item5 = "Отзывы"
        kb3.add(item1, item2, item3, item4, item5)
        bot.send_message(message.from_user.id, "Выберите категорию", reply_markup=kb3)
        bot.register_next_step_handler(message, rooms_selection, hotel)
    if message.text == "Изменить отзыв":
        kb1 = types.ReplyKeyboardMarkup(True, True)
        item5 = "назад"
        kb1.add(item5, "1", "2", "3", "4", "5")
        bot.send_message(message.from_user.id, "Выберите оценку", reply_markup=kb1)
        bot.register_next_step_handler(message, change_stars, hotel)


def change_stars(message, hotel):
    """
    Изменение оценки пользователя

    :param message: сообщение
    :param hotel: определённый отель
    :return:
    """


    stars = message.text

    bot.send_message(message.from_user.id, 'Отредактируйте отзыв')
    bot.register_next_step_handler(message, change_review, hotel, stars)


def change_review(message,hotel,stars):
    """
    Изменение отзыва и обновение общего рейтинга

    :param message: сообщение
    :param hotel: определённый отель
    :param stars: изменённая оценка пользователя
    :return:
    """

    review = message.text
    main.review_update(message.from_user.id, hotel, stars, review)
    x = []
    for i in main.rating(hotel):
        x.append(i[0])
    y = sum(x) / len(x)
    main.average_rating(hotel, y)
    kb3 = types.ReplyKeyboardMarkup(True, True)

    item1 = "Назад"
    item2 = "На главное меню"
    item3 = "Свободные номера"
    item4 = "Занятые номера"
    item5 = "Отзывы"
    kb3.add(item1, item2, item3, item4, item5)

    bot.send_message(message.from_user.id, "Ваш комментарий изменён", reply_markup=kb3)
    bot.register_next_step_handler(message, rooms_selection, hotel)



def room(message,hotel):
    """
    выбор комнаты

    :param message: сообщение
    :param hotel: определённый отель
    :return:
    """
    if message.text == "назад":

        kb3 = types.ReplyKeyboardMarkup(True, True)

        item1 = "Назад"
        item2 = "На главное меню"
        item3 = "Свободные номера"
        item4 = "Занятые номера"
        item5 = "Отзывы"
        kb3.add(item1, item2, item3, item4, item5)


        bot.send_message(message.from_user.id, "Выберите категорию",reply_markup=kb3)
        bot.register_next_step_handler(message, rooms_selection, hotel)


    elif main.qwerty(hotel,message.text)[0][0] == "свободно":
        room = message.text
        full_info = main.show_room(message.text,hotel)[0]
        kb6 = types.ReplyKeyboardMarkup(True, True)
        item1 = "назад"
        item2 = "В главное меню"
        item3 = "Забранировать"
        kb6.add(item1,item2,item3)
        bot.send_photo(message.from_user.id, photo=full_info[-1], caption=f'описание: {full_info[0]}\n\n цена: {full_info[1]}',
                       reply_markup=kb6)
        bot.register_next_step_handler(message,choice,hotel,room)
    else:
        room = message.text
        full_info = main.show_room(message.text, hotel)[0]
        kb7 = types.ReplyKeyboardMarkup(True, True)
        item1 = "назад"
        item2 = "В главное меню"
        kb7.add(item1, item2)
        bot.send_photo(message.from_user.id, photo=full_info[-1], caption=f'описание: {full_info[0]}\n\n цена: {full_info[1]}',
                       reply_markup=kb7)
        bot.register_next_step_handler(message, choice, hotel, room)

def choice(message,hotel,room):
    """
    Решение юронирование или нет

    :param message: сообщение
    :param hotel: определённый отель
    :param room: комната выбранная клиентом
    :return:
    """
    if message.text == "Забранировать":
        main.add_to_cart(message.from_user.id,room,hotel)
        main.qwerty_update(hotel,room)
        bot.send_message(message.from_user.id, "добавлено в вашу карточку")

        kb = types.ReplyKeyboardMarkup(True, True)
        item1 = "Отели"
        item2 = "Информация"
        kb.add(item1, item2)

        bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=kb)

    if message.text == "назад":

        kb3 = types.ReplyKeyboardMarkup(True, True)

        item1 = "Назад"
        item2 = "На главное меню"
        item3 = "Свободные номера"
        item4 = "Занятые номера"
        item5 = "Отзывы"
        kb3.add(item1, item2, item3, item4, item5)

        bot.send_message(message.from_user.id, "Выберите категорию",reply_markup=kb3)
        bot.register_next_step_handler(message,rooms_selection,hotel)

    if message.text == "В главное меню":
        kb = types.ReplyKeyboardMarkup(True, True)
        item1 = "Отели"
        item2 = "Информация"
        kb.add(item1, item2)

        bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=kb)








if __name__ == "__main__":
    bot.polling()