from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from botCreate import dp, bot
from aiogram.dispatcher.filters import Text
from config import Admin_id
from database import sqlite_db as db
from keyboards import admin_keyboard, client_keyboard




class FSMAdmin(StatesGroup):
    cl_photo = State()
    cl_type=State()
    cl_brand=State()
    cl_model=State()
    cl_size=State()
    cl_price=State()
    cl_amount=State()

# Проверка пользователя на администратора
# dp.message_handler(commands=['moderator'])
async def admin_initialization(message: types.Message):
    if (message.chat.id in Admin_id):
        await bot.send_message(message.from_user.id, "Слушаюсь и повинуюсь!", reply_markup=admin_keyboard.button_case_admin)
        await message.delete()
    else:
        await bot.send_message(message.from_user.id, "Ты не мой повелитель!")
        await message.delete()

async def admin_to_client_initialization(message: types.Message):
    if (message.chat.id in Admin_id):
        await bot.send_message(message.from_user.id, "Хорошо. Вот меню смертных", reply_markup=client_keyboard.client_keyboard)
        await message.delete()
    else:
        await bot.send_message(message.from_user.id, "Ты не мой повелитель!")
        await message.delete()
    

# Начало диалога загрузки пункта меню
#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if (message.chat.id in Admin_id):
        await FSMAdmin.cl_photo.set()
        await message.reply('Загрузите фото')

# Картинка
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.cl_photo)
async def load_photo(message: types.Message, state=FSMContext):
    if (message.chat.id in Admin_id):
        async with state.proxy() as data:
            data['cl_photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Введите тип одежды")

# Тип одежды
#@dp.message_handler(state=FSMAdmin.cl_type)
async def load_type(message: types.Message, state=FSMContext):
    if (message.chat.id in Admin_id):
        async with state.proxy() as data:
            data['cl_type'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите наименование бренда одежды")

# Бренд одежды
#@dp.message_handler(state=FSMAdmin.cl_brand)
async def load_brand(message: types.Message, state=FSMContext):
    if (message.chat.id in Admin_id):
        async with state.proxy() as data:
            data['cl_brand'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите модель")


# Модель
#@dp.message_handler(state=FSMAdmin.cl_brand)
async def load_model(message: types.Message, state=FSMContext):
    if (message.chat.id in Admin_id):
        async with state.proxy() as data:
            data['cl_model'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите размер одежды")


# Размер одежды
#@dp.message_handler(state=FSMAdmin.cl_size)
async def load_size(message: types.Message, state=FSMContext):
    if (message.chat.id in Admin_id):
        async with state.proxy() as data:
            data['cl_size'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите цену")

# Цена
#@dp.message_handler(state=FSMAdmin.cl_price)
async def load_price(message: types.Message, state=FSMContext):
    if (message.chat.id in Admin_id):
        async with state.proxy() as data:
            data['cl_price'] = message.text
        await FSMAdmin.next()
        await message.reply("Введите количество товара")
        

async def load_amount(message: types.Message, state=FSMContext):
    if (message.chat.id in Admin_id):
        if message.text.isdigit():
            photo=await db.sql_find_photo(state)
            print("photo= "+str(photo))
            print("photo[0]= "+str(photo[0]))
            print("photo[0][0]= "+str(photo[0][0]))
            amount=int(message.text)
            for i in range(amount):
                if str(photo).replace('[]','')!='':
                    await db.sql_add_clothes(photo[0][0],state)
                else:
                    async with state.proxy() as data: 
                        print(str(tuple(data.values())[0]))
                        await db.sql_add_clothes(tuple(data.values())[0], state)
        else:
            print("Error message.text")




# Вывод полученной информации, хранящейся в памяти бота
    async with state.proxy() as data:
        await message.reply(str(data))
    # Завершение всего стака
    await state.finish()


    # Функция отмены действия бота
# @dp.message_handler(state="*", commands="отмена")
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def load_cancel(message: types.Message, state: FSMContext):
    if (message.chat.id in Admin_id):    
        current_state= await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


# Функция возврата в меню клиента


# Регистрация хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)    
    dp.register_message_handler(load_photo, content_types=['photo'],state=FSMAdmin)
    dp.register_message_handler(load_type, state=FSMAdmin.cl_type)
    dp.register_message_handler(load_brand, state=FSMAdmin.cl_brand)
    dp.register_message_handler(load_model, state=FSMAdmin.cl_model)
    dp.register_message_handler(load_size, state=FSMAdmin.cl_size)
    dp.register_message_handler(load_price, state=FSMAdmin.cl_price)
    dp.register_message_handler(load_amount, state=FSMAdmin.cl_amount)
    dp.register_message_handler(load_cancel, state="*", commands='отмена')
    dp.register_message_handler(load_cancel, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(admin_initialization, commands=['Администратор'])
    dp.register_message_handler(admin_to_client_initialization, commands=['Пользователь'])









    
