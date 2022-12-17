from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

b1=KeyboardButton('Режим работы')
b2=KeyboardButton('Доставка')
b3=KeyboardButton('Каталог')
b4=KeyboardButton('/Связаться_со_мной', request_contact=True)
b5=KeyboardButton('/Узнать_где_я', request_location=True)


# resize_keyboard делает клавиатуру меньше,
# а ome_time_keyboard позволяет спрятать клавиатуру после выбора
kb_client=ReplyKeyboardMarkup(resize_keyboard=True)
# Метод add просто добавляет кнопку в новую строку. 
# insert добавляет в новый столбец
client_keyboard=kb_client.add(b3).add(b1).insert(b2).add(b4).insert(b5)

# Добавление кнопок в строку
#kb_client.row(b1,b2,b3)