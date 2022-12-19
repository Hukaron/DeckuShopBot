from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.dispatcher import filters
from botCreate import dp, bot
from keyboards import client_keyboard, inline_keyboards as ikb
from database import sqlite_db as db
from keyboards.inline_keyboards import ikb_keyboard

# Прописывание обработчиков для клиентов
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятных покупок!', reply_markup=client_keyboard.client_keyboard)
        await message.delete()
    except:
        await message.reply('Общение с ботом невозможно в таком режиме!')

async def work_time(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Работает по будням. Заказы принимаются до 18.00')
        await message.delete()
    except:
        await message.reply('Общение с ботом невозможно в таком режиме!')

async def delivery_command(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Забрать вещи можно по адресу сети магазинов или мы отправим Вам заказ по почте')
        await message.delete()
    except:
        await message.reply('Общение с ботом невозможно в таком режиме!')

async def types_view(message: types.Message):
    await ikb.view_types(message)
    await message.delete()

async def cart_view(message: types.Message):
    await ikb.view_cart(message.from_user.id)
    await message.delete()

async def orders_order(message: types.Message):
    user_id=message.from_user.id
    price=0
    clothes_id_in_cart_of_user= await db.sql_view_cart(user_id)
    if str(clothes_id_in_cart_of_user).replace('[]','')!='':
        order_id= await db.sql_add_to_order(user_id)
        message_text='Товары в заказе № '+str(order_id[0][0])+':\n'
      #  await bot.send_message(user_id,'Товары в заказе № '+str(order_id[0][0])+':')
        for id in clothes_id_in_cart_of_user:
            clothes= await db.sql_clothes_by_id(id[0])
            for each in clothes:
                price+=each[5]
                message_text+=f'{each[1]} {each[2]}; Модель:{each[3]}; Размер:{each[4]}; Цена: {each[5]} \n'
               # await bot.send_photo(user_id, each[0], f'{each[1]} {each[2]}; Модель:{each[3]}; Размер:{each[4]}; Цена: {each[5]}')
                await db.sql_add_to_cl_odr(order_id[0][0], id[0])
                await db.sql_delete_from_cart(user_id, id[0])
        message_text+=f'Общая цена заказа: {price}'
        await bot.send_message(user_id,message_text)
        await db.sql_add_price_for_order(price,order_id[0][0])
    else:
        await bot.send_message(user_id, 'Ваша корзина пуста. Добавьте товары в корзину для формирования заказа')
    await message.delete()
        




async def orders_view(message: types.Message):
    user_id=message.from_user.id
    number_of_orders=await db.sql_find_all_orders(user_id)
    if str(number_of_orders).replace('[]','')!='':
        for order in number_of_orders:
            message_text='Товары в заказе № '+str(order[0])+':\n'
           # await bot.send_message(user_id, 'Заказ №:'+str(order[0])+' от '+order[1])
            all_clothes= await db.sql_clothes_in_orders(order[0])
            for each in all_clothes:
                message_text+=f'{each[1]} {each[2]}; Модель:{each[3]}; Размеры:{each[4]}; Цена: {each[5]} \n'
               # await bot.send_message(user_id, f'{each[1]} {each[2]}; Модель:{each[3]}; Размеры:{each[4]}; Цена: {each[5]}')
            message_text+=f'Цена заказа: {order[2]}'
            await bot.send_message(user_id, message_text)
    else:
        await bot.send_message(user_id, 'Ваша корзина пуста. Добавьте товары в корзину для формирования заказа')
    await message.delete()



# Вызов обработчиков через функцию используя диспатчер
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(work_time, text=['Режим работы'])
    dp.register_message_handler(delivery_command, text=['Доставка'])
    dp.register_message_handler(types_view, text=['Каталог'])
    dp.register_message_handler(cart_view, text=['Показать корзину'])
    dp.register_message_handler(orders_order, text=['Оформить заказ'])
    dp.register_message_handler(orders_view, text=['Показать мои заказы'])

