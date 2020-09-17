import mysqldatabase
import datetime
from telebot import types
import telebot
import config
import Items
bot = telebot.TeleBot(config.TOKEN)
choose_item = ''

@bot.message_handler(commands=['start'])
def process_start_command1(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton(text="Заполнить свое расписание")
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Выберите действие ', reply_markup=keyboard)



# @bot.message_handler(commands=['add'])
# def process_start_command1(message):
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     button_hm_next_day = types.InlineKeyboardButton(text="Next day", callback_data='nextday')
#     button_hm_choose = types.InlineKeyboardButton(text="Choose day", callback_data='chooseday')
#
#     keyboard.add(button_hm_choose, button_hm_next_day)
#
#     bot.send_message(message.chat.id, 'На какой день записывать?', reply_markup=keyboard)

@bot.message_handler(func=lambda call: True)
def button_starts(message):
    try:
        if message.text == 'Заполнить свое расписание':
            # for school_day in Items.school_days:
            #     bot.send_message(message.chat.id, school_day)
            #     bot.send_message(message.chat.id, 'Первый урок: ')
            #     bot.register_next_step_handler(msg, save_home_work)
            markup = types.InlineKeyboardMarkup()
            buttons = []
            for number_1 in range(0, len(Items.school_days_eng)):
                buttons.append(types.InlineKeyboardButton(text=textButton, callback_data=callbackButton))
            for button in buttons:
                markup.add(button)
            bot.send_message(message.chat.id, 'Выберите действие ', reply_markup=markup)
    except Exception as e:
        bot.reply_to(message.chat.id, 'Oppss')


# def fill_blank(message):
#     sql = "INSERT INTO customers (id, monday, tuesday, wednesday, thursday, friday, saturday) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#     val = (str(message.chat.id), 'русский;английский;фк;музыка', 'изо;английский;фк;музыка', 'русский;английский;фк;музыка', 'русский;английский;фк;музыка;биология;')
#     mysqldatabase.mycursor.execute(sql, val)
#     mysqldatabase.mydb.commit()



def save_home_work(message):
    global choose_item
    try:
        tomorrow = datetime.date.today() + datetime.timedelta(1)
        sql = "INSERT INTO customers (id, datetime, item, task) VALUES (%s, %s, %s, %s)"
        val = (str(message.chat.id), str(tomorrow), str(choose_item), str(message.text))
        mysqldatabase.mycursor.execute(sql, val)
        mysqldatabase.mydb.commit()
        bot.send_message(message.chat.id, 'Дз записано!')
        markup = types.ReplyKeyboardRemove(selective=True)
    except Exception as e:
        bot.reply_to(message.chat.id, 'Oppss')


@bot.callback_query_handler(func=lambda call: True)
def ChooseItem(call):
    global choose_item
    if call.message:
        if call.data == 'nextday':
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            button_russian = types.InlineKeyboardButton(text="Русский", callback_data='russian')
            button_mat = types.InlineKeyboardButton(text="Математика", callback_data='matematika')
            keyboard.add(button_russian, button_mat)
            bot.send_message(call.message.chat.id, 'Выберите предмет.', reply_markup=keyboard)
        if call.data == 'russian':
            choose_item = 'Russian'
            markup = types.ReplyKeyboardRemove(selective=True)
            msg = bot.send_message(call.message.chat.id, "Запиши: ")
            bot.register_next_step_handler(msg, save_home_work)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Next day', reply_markup=None)


bot.polling(none_stop=True, timeout=1000)
