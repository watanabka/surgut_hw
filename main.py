from telebot import types
import telebot
import config
import Items
import mysqldatabase
bot = telebot.TeleBot(config.TOKEN)
choose_item = ''
to_day = ''

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    write = types.KeyboardButton('Записать домашнее задание ')
    see = types.KeyboardButton('Просмотреть домашнее задание')
    markup.add(write, see)
    send_mess = f"Приветствуем, {message.from_user.first_name}! \nНаш бот для домашнего задание в вашем использование "
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(func=lambda call:True)
def write(message):
    try:
        if message.text == 'Записать домашнее задание':
            markup = types.InlineKeyboardMarkup()
            buttons = []
            for number_1 in range(0, len(Items.school_days_eng)):
                buttons.append(types.InlineKeyboardButton(text=Items.school_days[number_1], callback_data=Items.school_days_eng[number_1]))
            for button in buttons:
                markup.add(button)
            bot.send_message(message.chat.id, "На какой день недели будем записывать?", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message.chat.id, 'Упс..')

def showhm(message):
    global to_day
    global choose_item
    try:
        sql = "INSERT INTO customers (id, day, item, task) VALUES (%s, %s, %s, %s)"
        val = (str(message.chat.id), str(to_day), str(choose_item), str(message.text))
        mysqldatabase.mycursor.execute(sql, val)
        mysqldatabase.mydb.commit()
        bot.send_message(message.chat.id, 'Вы успешно записали домашнее задание по ' + choose_item + " на " + to_day)
        markup = types.ReplyKeyboardRemove(selective=True)
    except Exception as e:
        bot.reply_to(message.chat.id, 'Oppss')



def writehm(message):
    global to_day
    global choose_item
    try:
        if mysqldatabase.getday(str(message.chat.id)) == to_day and mysqldatabase.getitem(str(message.chat.id)) != choose_item:
            sql = "UPDATE customers SET item = %s WHERE id = %s"
            val = (str(message.chat.id), str(mysqldatabase.getitem(str(message.chat.id))) + ";" + str(choose_item))

            mysqldatabase.mycursor.execute(sql, val)
            mysqldatabase.mydb.commit()

            sql = "UPDATE customers SET task = %s WHERE id = %s"
            val = (str(message.chat.id), str(mysqldatabase.gettask(str(message.chat.id))) + ";" + str(message.text))

            mysqldatabase.mycursor.execute(sql, val)
            mysqldatabase.mydb.commit()

            bot.send_message(message.chat.id, 'Вы успешно записали домашнее задание по ' + choose_item + " на " + to_day)
            markup = types.ReplyKeyboardRemove(selective=True)
        else:
            sql = "INSERT INTO customers (id, day, item, task) VALUES (%s, %s, %s, %s)"
            val = (str(message.chat.id), str(to_day), str(choose_item), str(message.text))
            mysqldatabase.mycursor.execute(sql, val)
            mysqldatabase.mydb.commit()
            bot.send_message(message.chat.id, 'Вы успешно записали домашнее задание по ' + choose_item + " на " + to_day)
            markup = types.ReplyKeyboardRemove(selective=True)
    except Exception as e:
        bot.reply_to(message.chat.id, 'Oppss')

@bot.callback_query_handler(func=lambda call: True)
def ChooseItem(call):
    global to_day
    global choose_item
    if call.message:
        for number_1 in range(0, len(Items.school_item_rus)):
            if str(call.data) == str(Items.school_item_eng[number_1]):
                choose_item = Items.school_item_eng[number_1]
                msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=("Запишите задание на " + str(to_day) + " по " + str(Items.school_item_rus[number_1]) + ": "), reply_markup=None)
                bot.register_next_step_handler(msg, writehm)

        for number_2 in range(0, len(Items.school_days_eng)):
            if str(call.data) == str(Items.school_days_eng[number_2]):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите урок:', reply_markup=None)
                items_show(call.message)
                to_day = Items.school_days_eng[number_2]

def items_show(message):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for number_1 in range(0, len(Items.school_item_rus)):
        buttons.append(types.InlineKeyboardButton(text=Items.school_item_rus[number_1], callback_data=Items.school_item_eng[number_1]))
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, 'Выберите действие: ', reply_markup=markup)



bot.polling(none_stop=True)
