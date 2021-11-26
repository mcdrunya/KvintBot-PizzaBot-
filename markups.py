from telebot import types

# Главное меню
start_menu = types.ReplyKeyboardMarkup(True, True)
start_menu.row("🍕Заказать пиццу")

# Меню выбора пиццы
order_menu = types.ReplyKeyboardMarkup(True, True)
order_menu.row('Большую', 'Маленькую')
order_menu.row('⬅️Назад')

# Меню выбора способа оплаты
payment_menu = types.ReplyKeyboardMarkup(True, True)
payment_menu.row("💵Наличка", "💳Банковская карта")