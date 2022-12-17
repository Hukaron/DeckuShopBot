from aiogram import Bot
from aiogram.utils import executor
from botCreate import dp
from database import sqlite_db

#Вывод в консоли сообщения о начале работы
async def on_startup(_):
    print('Бот в работе')
    sqlite_db.sql_start()

#Подключение файлов-обоработчиков
from handlers import botClient, botAdmin, botForAll
from keyboards import inline_keyboards
#Запуск обработчиков для клиентов
botClient.register_handlers_client(dp)
botAdmin.register_handlers_admin(dp)
#Поллинг. Надстройки при запуске бота и отслеживание его работы.
#skip_updates- не обрабатывать запросы которые пришли выключенному боту. 
#on_startup- функция on_startup
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)