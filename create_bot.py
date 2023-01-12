from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from configs.config import TOKEN


bot = Bot(token = TOKEN)
dp = Dispatcher(bot)