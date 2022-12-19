from aiogram.dispatcher import FSMContext
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from botCreate import dp, bot
from database import sqlite_db as db
from aiogram.dispatcher.filters.state import State, StatesGroup

state=FSMContext

#Кнопка ссылка
ikb_keyboard=InlineKeyboardMarkup(row_width=3)
# Вывод всех категорий товара
async def view_types(message):
    clothes=await db.sql_search_types()
    ikb_keyboard=InlineKeyboardMarkup(row_width=3)
    for cl_type in clothes:
        button=InlineKeyboardButton(text=cl_type[0], callback_data=f'view {cl_type[0]}' )
        ikb_keyboard.insert(button)
    await message.answer('Категории товаров',reply_markup=ikb_keyboard)

@dp.callback_query_handler(lambda x:x.data and x.data.startswith('view '))
async def category_view(callback_query: types.CallbackQuery):
    cl_type=callback_query.data.replace('view ', '')
    clothes_from_db= await db.sql_view_catalog(cl_type)
    clothes_id=0
    for clothes in clothes_from_db:
        clothes_id=clothes_id+1
        clothes_amount= await db.sql_count_amount(clothes)
        clothes_sizes= await db.sql_find_all_sizes(clothes[1],clothes[3])
        all_sizes=str(clothes_sizes).replace('[(','').replace('(','').replace(',)','').replace(']','')
        sizes=all_sizes.split()
        await bot.send_photo(callback_query.from_user.id, clothes[0], f'{clothes[1]} {clothes[2]}\nМодель: {clothes[3]};\nРазмер: {all_sizes};\nЦена: {clothes[4]} рублей\nКоличество на складе: {str(clothes_amount)} шт.')
        zakaz_keyboard=InlineKeyboardMarkup(row_width=(len(clothes_sizes)))
        for each in clothes_sizes:
            button=InlineKeyboardButton(f'Размер {each[0]}', callback_data=f'cart {clothes[1]} {clothes[3]} {each[0]}')
            zakaz_keyboard.insert(button)
        await bot.send_message(callback_query.from_user.id, text=f'Заказать {clothes[1]}', reply_markup=zakaz_keyboard)




@dp.callback_query_handler(lambda x: x.data and x.data.startswith('cart '))
async def order_form(callback_query: types.CallbackQuery):
    clothes_info=callback_query.data.replace('cart ', '').split()
    clothes_id= await db.sql_find_id_of_size(clothes_info[0],clothes_info[1],clothes_info[2])
    user_id=callback_query.from_user.id
    if str(clothes_id).replace('[]','')!='':
        searches= await db.sql_search_in_cart(user_id, clothes_id[0][0])
        if str(searches).replace('[]','') =='':
            await db.sql_add_to_shopping_cart(user_id,clothes_id[0][0])
            await callback_query.answer('Товар добавлен в корзину!')
        else:
            await callback_query.answer('Товар уже в корзине')
    else: await callback_query.answer('Данный размер закончился')



async def view_cart(user_id):
    price=0
    clothes_id_in_cart_of_user= await db.sql_view_cart(user_id)
    if str(clothes_id_in_cart_of_user).replace('[]','')!='':
        await bot.send_message(user_id,'Товары в корзине:')
        for id in clothes_id_in_cart_of_user:
            clothes= await db.sql_clothes_by_id(id[0])
            for each in clothes:
                price+=each[5]
                await bot.send_photo(user_id, each[0], f'{each[1]} {each[2]}; Модель:{each[3]}; Размер:{each[4]}; Цена: {each[5]}', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton('Удалить из корзины', callback_data=f'del {id[0]}')))
        await bot.send_message(user_id,f'Общая цена корзины: {price}')
    else: await bot.send_message(user_id, 'Ваша корзина пуста')


# Баг на название фотографий. ОТдельно обращаться к фотографиям, отдельно к файлам
@dp.callback_query_handler(lambda x:x.data and x.data.startswith('del '))
async def clothes_delete_by_id(callback_query: types.CallbackQuery):
    clothes_id=callback_query.data.replace('del ', '')
    user_id=callback_query.from_user.id
    await db.sql_delete_from_cart(user_id, clothes_id[0])
    await view_cart(user_id)




async def ask_for_size(message: types.Message):
    async with state.proxy as data:
            data=message.text
            return data

def register_handlers_inkeyboards(dp: Dispatcher):
    dp.register_message_handler(ask_for_size, state, content_types=["text"])