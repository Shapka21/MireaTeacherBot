dict_days = {'понедельник': 0, 'вторник': 1, 'среда': 2,
             'четверг': 3, 'пятница': 4, 'суббота': 5}


def start_command_register():
    return 'Пожалуйста представьтесь, напиши свою фамилию.\n' \
           'Будьте внимательны, пожалуйста <b>проверьте</b> текст ' \
           'перед отправкой.'


def start_command_usual():
    return 'Я бот с расписанием МИРЭА для преподавателей.\n' \
           'Умею показывать пары преподавателя на этой неделе.'


def menu_command():
    return 'Воспользуйтесь встроенными функциями для навигации по боту.'


def help_command():
    return 'Воспользуйтесь командой /menu для отображения кнопок.\n' \
           'Команда /change_name поможет вам сменить имя.'


def response_notion_url():
    return 'Cсылка на Notion'


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


def request_type_of_schedule():
    return 'Какое именно расписание необходимо вывести?'


def request_name_mess():
    return 'Введите фамилию преподавателя'


def unknown_week():
    return 'На этой неделе расписания пока нет'


def unknown_day():
    return 'Сегодня в расписании пар нет'


def unknown_lessons():
    return 'У данного преподавателя больше нет пар на этой неделе'


def unknown_teacher():
    return 'Извините, данный преподаватель не найден'


def unknown_memory_teacher():
    return 'Извините, указанный ранее преподаватель не найден'


def unknown_not_registered_teacher():
    return 'Запрос не возможно выполнить, необходимо определить фамилию. ' \
           'Воспользуйтесь командой /change_name.'


def unknown_mess_text():
    return 'Извините, не могу вас понять.\n' \
           'Воспользуйтесь командой /help и встроенными кнопками.'
