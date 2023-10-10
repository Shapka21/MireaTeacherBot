dict_days = {'понедельник': 0, 'вторник': 1, 'среда': 2,
             'четверг': 3, 'пятница': 4, 'суббота': 5}


def start_command():
    return 'Я бот с расписанием МИРЭА для преподавателей.\n' \
           'Умею показывать пары преподавателя на этой неделе.'


def help_command():
    return 'Воспользуйтесь командой /start'


def response_notion_url():
    # Изменить текст
    return 'Вот ваш notion url'


def response_schedule_wait():
    return 'Ожидайте ⏳'


def response_schedule(day, day_schedule):
    ans = [f'<b>{day.upper()}</b>']
    for lesson in day_schedule:
        ans.append(f'<b>{lesson[0]}. {lesson[1]}</b>\n' \
                   f'<code>Аудитория:</code> {lesson[2]}\n' \
                   f'<code>Группа:</code> {lesson[3]}\n'
                   f'<code>Комментарий:</code> {lesson[4]}')
    return f'\n——————————\n'.join(ans)


def request_name_mess():
    return 'Введите фамилию преподавателя'


def unknown_week():
    return 'На этой неделе расписании пока нет'


def unknown_lessons():
    return 'У данного преподавателя больше нет пар на этой неделе'


def unknown_teacher():
    return 'Извините, данный преподаватель не найден'


def unknown_mess_text():
    return 'Извините, не могу вас понять.\n' \
           'Воспользуйтесь командой /start'