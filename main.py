import markups
import telebot
import os
from telebot import types
from replit import db

token = os.environ['token']

bot = telebot.TeleBot(token)

print("Бот готов к работе!")


def get_or_create_user(user_id:str):
  if db.get(user_id) is None:
    db[user_id] = {"user_id": user_id, "order": "", "payment_method": ""}
  
  return db.get(user_id)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Добро пожаловать в бота для заказа пиццы!', reply_markup=markups.start_menu)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    
    if message.text == '🍕Заказать пиццу':
        bot.send_message(message.from_user.id, 'Меню → Заказ\nКакую вы хотите пиццу?', reply_markup=markups.order_menu)

    elif message.text.lower() == 'большую':
        payment_menu(message) # выбор способа оплаты

    elif message.text.lower() == 'маленькую':
        payment_menu(message)

    elif message.text == '⬅️Назад':
        start_menu(message) # возвращение в "главное меню"

        
def start_menu(message):
    bot.send_message(message.from_user.id, 'Главное меню', reply_markup=markups.start_menu)


def payment_menu(message):
    user = get_or_create_user(str(message.from_user.id))
    user["order"] = message.text
    bot.send_message(message.from_user.id, 'Как вы будете платить\nНаличкой или картой?', reply_markup=markups.payment_menu)
    bot.register_next_step_handler(message, get_info)


def back_to_payment(message):
    bot.register_next_step_handler(message, get_info)
    

def get_info(message):
    user = get_or_create_user(str(message.from_user.id))
    lst_payment_method = ['наличка', 'банковская карта', 'карта', 'картой', 'наличкой']

    payment_method = message.text.lower().strip('💵💳')
    if payment_method in lst_payment_method:
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Подтвердить✅', callback_data='yes') 
        keyboard.add(key_yes) #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='Отменить✖️', callback_data='no')
        keyboard.add(key_no)
        
        question = f"Вы хотите {user['order'].lower()} пиццу, оплата - {payment_method.lower()}"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        del db[str(message.from_user.id)]
    else:
        bot.send_message(message.from_user.id, "Указан неверный способ оплаты!\nПопробуйте еще раз.")
        return back_to_payment(message)


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
