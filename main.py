from unittest import result
import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('TOKEN')

conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()

user_data= {
    'login': '',
    'password': '',
    'source': '',
    'other_source': '',
}

user_name = {
    'usr_name': ''
}

def db_table_val(login: str, password: str, source: str):
    cursor.execute('INSERT INTO log_pass (login, password, source) VALUES (?, ?, ?)', (login, password, source))
    conn.commit()


@bot.message_handler(commands='start')
def regisntration(message):

    usr_name = message.from_user.username

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {usr_name} (login STRING, password STRING, source STRING)''')
    conn.commit()

    bot.send_message(message.chat.id, "Привет, я бот который будет сохранять твои пароли. Когда ты нажал на /start я зарегистрировал тебя.\nТеперь можем записать твои пароли!")
    start_message(message)

@bot.message_handler(content_types='text')
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    add = types.KeyboardButton('Добавить пароль')
    item1 = types.KeyboardButton('ВК')
    item2 = types.KeyboardButton('Google')
    item3 = types.KeyboardButton('Apple ID')
    item4 = types.KeyboardButton('Другие пароли')
    item5 = types.KeyboardButton('Удалить пароль')
    

    markup.add(add, item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, 'Какой пароль тебе подсказать?', reply_markup=markup)

    bot.register_next_step_handler(message, keyboard)
    
def keyboard(message):
    if message.text == 'Добавить пароль':
        login_add(message)
    elif message.text == 'ВК':
        vk_show_pass(message)
    elif message.text == 'Google':
        google_show_pass(message)
    elif message.text == 'Apple ID':
        apID_show_pass(message)
    elif message.text == 'Другие пароли':
        other_show_pass(message)
    elif message.text == 'Удалить пароль':
        delote_step0(message)

#метод удаления данных из БД
def delote_step0(message):
    markup_3 = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1_3 = types.KeyboardButton('ВК')
    item2_3 = types.KeyboardButton('Google')
    item3_3 = types.KeyboardButton('Apple ID')
    item4_3 = types.KeyboardButton('Другое')

    markup_3.add(item1_3, item2_3, item3_3, item4_3)

    delite_1 = bot.send_message(message.chat.id, 'Отчего удалить пароль?', reply_markup=markup_3)
    bot.register_next_step_handler(delite_1, delite)
    
def delite(message):
    if message.text == 'Другое':
        delite_other(message)
    else:
        user_name = message.from_user.username
        cursor.execute(f"SELECT * FROM {user_name}")
        # gолучаем результат сделанного запроса
        results = cursor.fetchall()
        login = message.text
        print(results)
        bot.send_message(message.chat.id, "Вот твои пароли:")
        # проверяем есть ли совпадения в базе данных по запросу нужного пароля
        for i in results:
            if login in i:
                msg_login =  (i[0])
                msg_pass = (i[1])
                bot.send_message(message.chat.id, 'login')
                bot.send_message(message.chat.id, msg_login)
                bot.send_message(message.chat.id, 'password')
                bot.send_message(message.chat.id, msg_pass)
                bot.send_message(message.chat.id, '🔗'*9)
            else:
                print('Not found')
        
        msg = bot.send_message(message.chat.id, 'Введи логин от пары log|pass котрую хочешь удалить:')
        bot.register_next_step_handler(msg, delite_step1)

def delite_step1(message):
    markup_3 = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1_3 = types.KeyboardButton('/start')


    markup_3.add(item1_3)

    bot.send_message(message.chat.id, 'Если хочешь вернуться домой нажми кнопку', reply_markup=markup_3)

    user_name = message.from_user.username
    cursor.execute(f"SELECT * FROM {user_name}")
    #получаем результат сделанного запроса
    results = cursor.fetchall()
    print(results)
    login = message.text
    # проверяем есть ли совпадения в базе данных по запросу нужного пароля
    for i in results:
        if login in i:
            sql_update_query = f"""DELETE from {user_name} where login = ?"""
            cursor.execute(sql_update_query, (login, ))
            bot.send_message(message.chat.id, 'Логин и пароль успешно удалены!')
                     
def google_show_pass(message):
    user_name = message.from_user.username
    cursor.execute(f"SELECT * FROM {user_name}")
    # gолучаем результат сделанного запроса
    results = cursor.fetchall()
    name = message.text
    # проверяем есть ли совпадения в базе данных по запросу нужного пароля
    for i in results:
        if name in i:
            msg_login =  (i[0])
            msg_pass = (i[1])
            bot.send_message(message.chat.id, 'login')
            bot.send_message(message.chat.id, msg_login)
            bot.send_message(message.chat.id, 'password')
            bot.send_message(message.chat.id, msg_pass)
            bot.send_message(message.chat.id, '🔗'*9)

        else:
            print('Not found')
    
    start_message(message)

def vk_show_pass(message):
    user_name = message.from_user.username
    cursor.execute(f"SELECT * FROM {user_name}")
    # Получаем результат сделанного запроса
    results = cursor.fetchall()
    name = message.text
    # проверяем есть ли совпадения в базе данных по запросу нужного пароля
    for i in results:
        if name in i:
            msg_login =  (i[0])
            msg_pass = (i[1])
            bot.send_message(message.chat.id, 'login')
            bot.send_message(message.chat.id, msg_login)
            bot.send_message(message.chat.id, 'password')
            bot.send_message(message.chat.id, msg_pass)
            bot.send_message(message.chat.id, '🔗'*9)

        else:
            print('Not found')
    
    start_message(message)

def apID_show_pass(message):
    user_name = message.from_user.username
    cursor.execute(f"SELECT * FROM {user_name}")
    # Получаем результат сделанного запроса
    results = cursor.fetchall()
    name = message.text
    # проверяем есть ли совпадения в базе данных по запросу нужного пароля
    for i in results:
        if name in i:
            msg_login =  (i[0])
            msg_pass = (i[1])
            bot.send_message(message.chat.id, 'login')
            bot.send_message(message.chat.id, msg_login)
            bot.send_message(message.chat.id, 'password')
            bot.send_message(message.chat.id, msg_pass)
            bot.send_message(message.chat.id, '🔗'*9)

        else:
            print('Not found')
    
    start_message(message)

def login_add(message):
    login = bot.send_message(message.chat.id, 'Введи логин')
    bot.register_next_step_handler(login, password_add)
    
def password_add(message):
    user_data['login']=message.text
    password = bot.send_message(message.chat.id, 'Введи пароль')
    bot.register_next_step_handler(password, source_add)
    print(user_data['login'])

def source_add(message):
    user_data['password']=message.text
    print(user_data['password'])
    markup_2 = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1_1 = types.KeyboardButton('ВК')
    item2_2 = types.KeyboardButton('Google')
    item3_3 = types.KeyboardButton('Apple ID')
    item4_4 = types.KeyboardButton('Другие')

    markup_2.add(item1_1, item2_2, item3_3, item4_4)

    source = bot.send_message(message.chat.id, 'Отчего пароль?', reply_markup=markup_2)


    bot.register_next_step_handler(source, add_db)

def add_db(message):
    if message.text == 'Другие':
        other_add_table_pass(message)

    else:
        user_data['source']=message.text
        get_log_pass(message)
        print(user_data['source'])
        message = bot.send_message(message.chat.id, 'Данные успешно добавлены')
        start_message(message)
    
def get_log_pass(message):
    user_name = message.from_user.username
    cursor.execute(f'insert into {user_name} values (?,?,?)', [user_data['login'], user_data['password'], user_data['source']])
    conn.commit()
    print('чёт изи невспотел')
    
def text(message):
    bot.send_message(message.chat.id, 'Я тебя не понимаю, выбери что-то из клавиатуры.')
    start_message(message)

def other_add_table_pass(message):
    usr_name = message.from_user.username
    #создаем отдельную таблицу для других паролей
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {usr_name+'_other_log_pass'} (login STRING, password STRING, source STRING, other_source STRING)''')
    
    print('Таблица для "ДРУГИХ" создана')

    msg = bot.send_message(message.chat.id, 'Комментарий к паролю? (Например, отчего он)')
    bot.register_next_step_handler(msg, other_add_pass)

def other_add_pass(message):
    user_data['source']=='Óther'
    user_data['other_source']=message.text
    usr_name = message.from_user.username
    cursor.execute(f"insert into {usr_name+'_other_log_pass'} values (?,?,?,?)", [user_data['login'], user_data['password'], user_data['source'], user_data['other_source']])
    conn.commit()
    print('Добавил пароль в другую категорию')
    bot.send_message(message.chat.id, 'Пароль успешно добавлен.')
    start_message(message)

def other_show_pass(message):
    # gолучаем результат сделанного запроса
    usr_name = message.from_user.username
    cursor.execute(f"SELECT * FROM {usr_name+'_other_log_pass'}")
    conn.commit()
    results = cursor.fetchall()
    print(results)
    # проверяем есть ли совпадения в базе данных по запросу нужного пароля
    for i in results:
        msg_login =  (i[0])
        msg_pass = (i[1])
        msg_comment = (i[3])
        bot.send_message(message.chat.id, 'Комментарий к паролю')
        bot.send_message(message.chat.id, msg_comment)
        bot.send_message(message.chat.id, 'login')
        bot.send_message(message.chat.id, msg_login)
        bot.send_message(message.chat.id, 'password')
        bot.send_message(message.chat.id, msg_pass)
        bot.send_message(message.chat.id, '🔗'*9)

        
        print('Not found')
    
    start_message(message)

def delite_other(message):
    usr_name = message.from_user.username
    cursor.execute(f"SELECT * FROM {usr_name+'_other_log_pass'}")
    # gолучаем результат сделанного запроса
    results = cursor.fetchall()
    print(results)
    bot.send_message(message.chat.id, "Вот твои пароли:")
    # проверяем есть ли совпадения в базе данных по запросу нужного пароля
    for i in results:
        msg_login_other =  (i[0])
        msg_pass_other = (i[1])
        msg_comment = (i[3])
        bot.send_message(message.chat.id, 'Комментарий к паролю')
        bot.send_message(message.chat.id, msg_comment)
        bot.send_message(message.chat.id, 'login')
        bot.send_message(message.chat.id, msg_login_other)
        bot.send_message(message.chat.id, 'password')
        bot.send_message(message.chat.id, msg_pass_other)
        bot.send_message(message.chat.id, '🔗'*9)

    
    msg_2 = bot.send_message(message.chat.id, 'Введи комментарий от пары log|pass и я удалю эту пару:')
    bot.register_next_step_handler(msg_2, delite_step1_other)

def delite_step1_other(message):

    usr_name = message.from_user.username
    markup_5 = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1_5 = types.KeyboardButton('/start')

    markup_5.add(item1_5)

    bot.send_message(message.chat.id, 'Если хочешь вернуться домой нажми кнопку', reply_markup=markup_5)

    
    cursor.execute(f"SELECT * FROM {usr_name+'_other_log_pass'}")
    #получаем результат сделанного запроса
    results = cursor.fetchall()
    print(results)
    login = message.text
    # проверяем есть ли совпадения в базе данных по запросу нужного пароля
    for i in results:
        if login in i:
            sql_update_query = f"""DELETE from {usr_name+'_other_log_pass'} where other_source = ?"""
            cursor.execute(sql_update_query, (login, ))
            bot.send_message(message.chat.id, 'Логин и пароль успешно удалены!')
                     
bot.polling(none_stop=True)
