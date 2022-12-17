from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from config import TOKEN
#Хранение данных в оперативной памяти
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Обозначение бота и диспатчера
storage=MemoryStorage()
bot=Bot(token=TOKEN)
dp=Dispatcher(bot, storage=storage)
