import mysqldatabase
import datetime
from telebot import types
import telebot
import config
bot = telebot.TeleBot(config.TOKEN)
choose_item = ''

@bot.message_handler(commands=['add'])
def process_start_command1(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_hm_next_day = types.InlineKeyboardButton(text="Next day", callback_data='nextday')
    button_hm_choose = types.InlineKeyboardButton(text="Choose day", callback_data='chooseday')

    keyboard.add(button_hm_choose, button_hm_next_day)

    bot.send_message(message.chat.id, 'На какой день записывать?', reply_markup=keyboard)

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
