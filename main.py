import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.executor import start_webhook

import re
from datetime import datetime

from configure.env import config
import texts
import sheets

bot = Bot(token=config['token'])
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                    selective=True)
main_keyboard.add("Notion")
main_keyboard.add("Получить расписание")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(texts.start_command(),
                         reply_markup=main_keyboard)


@dp.message_handler(lambda message: message.text == "Notion")
async def open_url(message: types.Message):
    notion_keyboard = InlineKeyboardMarkup()
    notion_keyboard.add(InlineKeyboardButton('Notion',
                                             url='https://www.notion.so/79df1097863c453e86849c5e1fdb2c77'))
    await bot.send_message(message.chat.id, texts.response_notion_url(),
                           reply_markup=notion_keyboard)


@dp.message_handler(lambda message: message.text == "Получить расписание")
async def get_schedule(message: types.Message):
    await bot.send_message(message.chat.id, texts.request_name_mess())


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer(texts.help_command())


@dp.message_handler()
async def all_message_handler(message: types.Message):
    cyrillic_pattern = r'^[А-Яа-я]+$'
    if re.match(cyrillic_pattern, message.text) \
            and 4 <= len(message.text) <= 14:
        await message.answer(texts.response_schedule_wait())
        current_date = datetime.now()
        schedule, no_teacher, no_week, day_diff = sheets.make_person_schedule(
            message.text, current_date)
        check_no_lessons = True
        await bot.delete_message(message.chat.id, message.message_id + 1)
        if no_teacher:
            check_no_lessons = False
            await message.answer(texts.unknown_teacher())
        elif no_week:
            check_no_lessons = False
            await message.answer(texts.unknown_week())
        elif schedule == {}:
            check_no_lessons = False
            await message.answer(texts.unknown_lessons())
        else:
            for week in schedule.keys():
                for day in schedule[week].keys():
                    if texts.dict_days[day] >= day_diff:
                        check_no_lessons = False
                        await message.answer(
                            texts.response_schedule(day, schedule[week][day]),
                            parse_mode='html')
        if check_no_lessons:
            check_no_lessons = True
            await message.answer(texts.unknown_lessons())
    else:
        await message.answer(texts.unknown_mess_text())


# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

async def on_startup(dp):
    webhook_url = config['url']
    await bot.set_webhook(webhook_url)


async def on_shutdown(dp):
    await bot.delete_webhook()


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path="/",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="localhost",
        port=8000,
    )