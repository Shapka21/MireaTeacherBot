import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from configure.env import config
bot = Bot(token=config['token'])
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


async def on_shutdown(dp):
    await bot.delete_webhook()


if __name__ == "__main__":
    from algorithms.handlers import dp, on_startup

    start_webhook(
        dispatcher=dp,
        webhook_path="/",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="localhost",
        port=8000,
    )
