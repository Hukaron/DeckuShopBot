from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from botCreate import dp, bot
from database import sqlite_db as db


#Кнопка ссылка
ikb_keyboard=InlineKeyboardMarkup(row_width=3)

async def view_types(message):
    clothes=await db.sql_search_types()
    ikb_keyboard=InlineKeyboardMarkup(row_width=3)
    for cl_type in clothes:
        button=InlineKeyboardButton(text=cl_type[0], callback_data=f'del {cl_type[0]}' )
        ikb_keyboard.add(button)
    await message.answer('Категории товаров',reply_markup=ikb_keyboard)

@dp.callback_query_handler(lambda x:x.data and x.data.startswith('del '))
async def category_view(callback_query: types.CallbackQuery):
    cl_type=callback_query.data.replace('del ', '')
    clothes_from_db= await db.sql_view_catalog(cl_type)
    clothes_id=0
    print(len(clothes_from_db))
    for clothes in clothes_from_db:
        clothes_id=clothes_id+1
        clothes_amount= await db.sql_count_amount(clothes)
        await bot.send_photo(callback_query.from_user.id, clothes[0], f'{clothes[1]} {clothes[2]}\nМодель: {clothes[3]};\nРазмер: {clothes[4]};\nЦена: {clothes[5]} рублей\nКоличество на складе: {str(clothes_amount)} шт.')
        await bot.send_message(callback_query.from_user.id, text='Заказ', reply_markup=InlineKeyboardMarkup().\
            add(InlineKeyboardButton('Добавить в заказ', callback_data=f'odr {clothes_id}')))

# Неправильно выводит searches
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('odr '))
async def order_form(callback_query: types.CallbackQuery):
    clothes_id=callback_query.data.replace('odr ', '')
    user_id=callback_query.from_user.id
    print(str(clothes_id)+" "+str(user_id))
    searches= await db.sql_search_in_cart(user_id, clothes_id)
    print(str(searches).replace('[]', ''))
    if str(searches).replace('[]','') =='':
        await db.sql_add_to_shopping_cart(user_id,clothes_id)
        await callback_query.answer('Товар добавлен в корзину!')
    else:
        await callback_query.answer('Товар уже в корзине')










