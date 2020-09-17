from telebot import types
import telebot
import config
import Items
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    write = types.KeyboardButton('Записать домашнее задание')
    see = types.KeyboardButton('Просмотреть домашнее задание')
    markup.add(write, see)
    send_mess = f"Приветствуем, {message.from_user.first_name} {message.from_user.last_name}! \nНаш бот для домашнего задание в вашем использование"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(func=lambda call:True)
def write(message):
    try:
        if message.text == 'Записать домашнее задание':
            keyboard = types.InlineKeyboardMarkup()
            monday = types.InlineKeyboardButton(text='Понедельник', callback_data ="monday")
            tuesday = types.InlineKeyboardButton(text='Вторник', callback_data ="tuesday")
            wednesday = types.InlineKeyboardButton(text='Среда', callback_data ="wednesday")
            thursday = types.InlineKeyboardButton(text='Четверг', callback_data ="thursday")
            friday = types.InlineKeyboardButton(text='Пятница', callback_data ="friday")
            saturday = types.InlineKeyboardButton(text='Суббота', callback_data ="saturday")
            keyboard.add(monday, tuesday, wednesday, thursday, friday, saturday)
            bot.send_message(message.chat.id, "На какой день недели будем записывать?", reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message.chat.id, 'Упс..')

@bot.callback_query_handler(func=lambda call: True)
def ChooseItem(call):
    if call.message:
        if call.data == 'monday':
            items_show(call.message)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите урок:', reply_markup=None)

def items_show(message):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for number_1 in range(0, len(Items.school_item_rus)):
        buttons.append(types.InlineKeyboardButton(text=Items.school_item_rus[number_1], callback_data=Items.school_item_rus[number_1]))
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, 'Выберите действие: ', reply_markup=markup)








bot.polling(none_stop=True)
