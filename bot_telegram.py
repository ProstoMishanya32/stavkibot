import aiogram
from create_bot import dp, bot
from aiogram import executor
import asyncio
from configs.config import member_id
from modules import parsing, sqlite_logic
async def on_startup(_):
    sqlite_logic.start()
    print('The bot was successfully launched!')
    await bot.send_message(member_id, "Парсинг запущен")
    await parsing.main()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)