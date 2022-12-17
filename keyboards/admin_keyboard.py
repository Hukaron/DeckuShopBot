from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from keyboards import client_keyboard
button_load=KeyboardButton('/Загрузить')
button_delete=KeyboardButton('/Удалить')

button_case_admin=ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete)