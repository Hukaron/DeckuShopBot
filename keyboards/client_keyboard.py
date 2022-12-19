from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

b1=KeyboardButton('Режим работы')
b2=KeyboardButton('Доставка')
b3=KeyboardButton('Каталог')
b4=KeyboardButton('Показать корзину')
b5=KeyboardButton('Оформить заказ')
b6=KeyboardButton('Показать корзину')
b7=KeyboardButton('Показать мои заказы')


# resize_keyboard делает клавиатуру меньше,
# а ome_time_keyboard позволяет спрятать клавиатуру после выбора
kb_client=ReplyKeyboardMarkup(resize_keyboard=True)
# Метод add просто добавляет кнопку в новую строку. 
# insert добавляет в новый столбец
client_keyboard=kb_client.add(b3).add(b6).add(b2).insert(b1).add(b5).insert(b7)

# Добавление кнопок в строку
#kb_client.row(b1,b2,b3)