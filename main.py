import markups
import telebot
from telebot import types   

with open('constants.txt') as f: #считываю ключ из файла
    token = f.readline()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Добро пожаловать в бота для заказа пиццы!', reply_markup=markups.start_menu)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == '🍕Заказать пиццу':
        bot.send_message(message.from_user.id, 'Меню → Заказ\nКакую вы хотите пиццу?', reply_markup=markups.order_menu)
    
    elif message.text.lower() == 'Большую'.lower():
        payment_menu(message) # выбор способа оплаты

    elif message.text.lower() == 'Маленькую'.lower():
        payment_menu(message)

    elif message.text == '⬅️Назад':
        start_menu(message) # возвращение в "главное меню"


def start_menu(message):
    bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markups.start_menu)

def payment_menu(message):
    global type_of_pizza
    type_of_pizza = message.text
    bot.send_message(message.from_user.id, 'Как вы будете платить\nНаличкой или картой?', reply_markup=markups.payment_menu)
    bot.register_next_step_handler(message, get_info)

def get_info(message):
    global payment_method
    payment_method = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Подтвердить✅', callback_data='yes') 
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Отменить✖️', callback_data='no')
    keyboard.add(key_no)
    question = f"Вы хотите {type_of_pizza.lower()} пиццу, оплата - {payment_method[1:].lower()}"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True) # обработчик ответов
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Спасибо за заказ!", reply_markup=markups.start_menu)   
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Отмена заказа.", reply_markup=markups.start_menu)

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id) # удаляет клавиатуру после выбора юзера


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True, interval=0)
