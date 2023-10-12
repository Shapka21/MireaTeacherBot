from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton
from datetime import datetime
import database.dbfunctions as db
import algorithms.sheets as sheets
import algorithms.texts as texts
import re

from main import bot, dp
from configure.env import config
from aiogram.dispatcher import FSMContext
from algorithms.userStates import UserStates

main_keyboard_1 = ReplyKeyboardMarkup(resize_keyboard=True,
                                      selective=True)
main_keyboard_1.add("Notion")
main_keyboard_1.add("Получить расписание")

main_keyboard_2 = ReplyKeyboardMarkup(resize_keyboard=True,
                                      selective=True)
main_keyboard_2.add("Расписание на день")
main_keyboard_2.add("Расписание на неделю")
main_keyboard_2.add("Поиск по преподавателю")


async def on_startup(dp):
    webhook_url = config['url']
    await bot.set_webhook(webhook_url)


@dp.message_handler(commands=['start'], state=None)
async def send_welcome(message: types.Message):
    await message.answer(texts.start_command_usual())
    if not db.check_in_data(str(message.from_user.id)):
        await db.make_user_profile(str(message.from_user.id))
        await message.answer(texts.start_command_register(), parse_mode='html')
        await UserStates.ChoseName.set()
    else:
        await send_menu(message)


@dp.message_handler(commands=['menu'], state=None)
async def send_menu(message: types.Message):
    await message.answer(texts.menu_command(),
                         reply_markup=main_keyboard_1)


@dp.message_handler(commands=['change_name'], state=None)
async def change_name(message: types.Message):
    await db.make_user_profile(str(message.from_user.id))
    await message.answer(texts.start_command_register(), parse_mode='html',
                         reply_markup=None)
    await UserStates.ChoseName.set()


@dp.message_handler(state=UserStates.ChoseName)
async def save_user_name(message: types.Message, state: FSMContext):
    if '/' not in message.text:
        await db.set_user_info_name(str(message.from_user.id), message.text)
        await message.answer(f'Фамилия сохранена')
    else:
        await message.answer(f'Не удалось сохранить фамилию')
    await message.answer(texts.menu_command(),
                         reply_markup=main_keyboard_1)
    await state.finish()


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer(texts.help_command())


@dp.message_handler(lambda message: message.text == "Notion")
async def open_url(message: types.Message):
    notion_keyboard = InlineKeyboardMarkup()
    notion_keyboard.add(InlineKeyboardButton('Notion',
                                             url='https://www.notion.so/'
                                                 '79df1097863c453e86849c'
                                                 '5e1fdb2c77'))
    await bot.send_message(message.chat.id, texts.response_notion_url(),
                           reply_markup=notion_keyboard)


@dp.message_handler(lambda message: message.text == "Получить расписание")
async def get_schedule(message: types.Message):
    await bot.send_message(message.chat.id, texts.request_type_of_schedule(),
                           reply_markup=main_keyboard_2)


@dp.message_handler(lambda message: message.text == "Расписание на день")
async def get_schedule_day(message: types.Message):
    if db.check_in_data(str(message.from_user.id)) and \
            (db.get_user_info_name(str(message.from_user.id))[0] is not None):
        wait_message = await message.answer(texts.response_schedule_wait())
        schedule, no_teacher, no_week, day_diff = get_schedule_data(
            str(message.from_user.id))
        await bot.delete_message(message.chat.id, wait_message.message_id)
        if no_week:
            await message.answer(texts.unknown_day())
        elif no_teacher:
            await message.answer(texts.unknown_memory_teacher())
        else:
            check_day = True
            for week in schedule.keys():
                for day in schedule[week].keys():
                    if texts.dict_days[day] == day_diff:
                        check_day = False
                        await message.answer(
                            texts.response_schedule(day, schedule[week][day]),
                            parse_mode='html')
            if check_day:
                check_day = True
                await message.answer(texts.unknown_day())
    else:
        await message.answer(texts.unknown_not_registered_teacher())


@dp.message_handler(lambda message: message.text == "Расписание на неделю")
async def get_schedule_week(message: types.Message):
    if db.check_in_data(str(message.from_user.id)) and \
            (db.get_user_info_name(str(message.from_user.id))[0] is not None):
        await get_schedule_week_template(message, True)
    else:
        await message.answer(texts.unknown_not_registered_teacher())


@dp.message_handler(lambda message: message.text == "Поиск по преподавателю")
async def get_schedule_by_name(message: types.Message):
    await message.answer(texts.request_name_mess())
    await UserStates.RequestSearchName.set()


@dp.message_handler(state=UserStates.RequestSearchName)
async def save_user_name(message: types.Message, state: FSMContext):
    cyrill_pattern = r'^[А-Яа-я]+$'
    if re.match(cyrill_pattern, message.text) and 4 <= len(message.text) <= 14:
        await get_schedule_week_template(message, False)
    else:
        await message.answer(texts.unknown_teacher())
    await state.finish()


def get_schedule_data(user_id='', request_name=''):
    if request_name == '':
        request_name = db.get_user_info_name(user_id)[0]
    current_date = datetime.now()
    schedule, no_teacher, no_week, day_diff = sheets.make_person_schedule(
        request_name, current_date)
    return schedule, no_teacher, no_week, day_diff


async def get_schedule_week_template(message, memory_request=False):
    await message.answer(texts.response_schedule_wait())
    if memory_request:
        schedule, no_teacher, no_week, day_diff = get_schedule_data(
            str(message.from_user.id))
    else:
        schedule, no_teacher, no_week, day_diff = get_schedule_data(
            str(message.from_user.id), message.text)
    check_no_lessons = True
    await bot.delete_message(message.chat.id, message.message_id + 1)
    if no_teacher:
        check_no_lessons = False
        if memory_request:
            await message.answer(texts.unknown_memory_teacher())
        else:
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
