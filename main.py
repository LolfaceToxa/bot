import telebot
from telebot import types

bot = telebot.TeleBot('1797429681:AAHttgclx3NswSKnAP_JuN-CA7_jj8aszhY')

name = ''
surname = ''
age = 0


@bot.message_handler(content_types=['text', 'document', 'audio'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name) # следующий шаг – функция get_name
    elif message.text == 'Привет' or message.text == 'привет':
        bot.send_message(message.from_user.id, "Доброго времени суток")
    elif message.text == 'Как дела?' or message.text == 'как дела??':
        bot.send_message(message.from_user.id, "Жив, цел, орёл")
    elif message.text == '=(':
        bot.send_message(message.from_user.id, "Не грусти")
        pic = "https://pp.userapi.com/c633626/v633626957/356c2/POvf4zwlOdA.jpg"
        bot.send_photo(message.from_user.id, pic)
    elif message.text == 'Уведомления ОРИОКС':
        bot.send_message(message.from_user.id, "В данный момент в разработке")
    else:
        bot.send_message(message.from_user.id, 'Ты такие вещи не говори...\nСписок команд:\n/reg\nПривет\nКак дела?\n=(\nУведомления ОРИОКС')


def get_name(message): # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup() # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes) # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    if age == 1:
        question = 'Тебе ' + str(age) + ' год, тебя зовут ' + name + ' ' + surname + '?'
    elif age > 4:
        question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    else:
        question = 'Тебе ' + str(age) + ' года, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Запомню : )')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Тогда всё по новой : (')


bot.polling(none_stop=True)