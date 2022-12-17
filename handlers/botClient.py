from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.dispatcher import filters
from botCreate import dp, bot
from keyboards import client_keyboard, inline_keyboards as ikb
from database import sqlite_db
from keyboards.inline_keyboards import ikb_keyboard

# Прописывание обработчиков для клиентов
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятных покупок!', reply_markup=client_keyboard.client_keyboard)
        await message.delete()
    except:
        await message.reply('Общение с ботом невозможно в таком режиме!')

async def open_command(message: types.Message):
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

async def view_types(message: types.Message):
    await ikb.view_types(message)
    await message.delete()


# Вызов обработчиков через функцию используя диспатчер
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(open_command, text=['Режим работы'])
    dp.register_message_handler(delivery_command, text=['Доставка'])
    dp.register_message_handler(view_types, text=['Каталог'])

