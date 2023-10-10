import gspread
from google.oauth2.service_account import Credentials
from configure.env import config
from datetime import datetime

googleapis_url = 'https://www.googleapis.com/auth/spreadsheets'
creds = Credentials.from_service_account_file(config['google_api_json'],
                                              scopes=[googleapis_url])
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(config['sheet_id'])


def get_sheet_titles(time):
    current_year = datetime.now().year
    sheet_titles = [i.title for i in spreadsheet.worksheets()]
    sheet_titles = [i for i in sheet_titles if ('Чет' in i) or ('Неч' in i)]
    for i in sheet_titles:
        time_list = ((i.split()[-1])[1:-1]).split('-')
        time_objects = []
        for j in time_list:
            if '.' in j:
                day, month = map(int, j.split('.'))
            else:
                day, month = map(int, j.split(','))
            date_object = datetime(current_year, month, day)
            time_objects.append(date_object)
        if (time >= time_objects[0]) and (time <= time_objects[1]):
            time_difference = time - time_objects[0]
            return [[i], time_difference.days]
    return None


def make_precursors(sheet_titles, teachers_name):
    titles_data = dict()

    for title in sheet_titles:
        title_data = spreadsheet.worksheet(title)

        days_column_data = title_data.col_values(1)
        lesson_num_column_data = title_data.col_values(2)
        subject_column_data = title_data.col_values(5)
        teacher_column_data = title_data.col_values(7)
        classroom_column_data = title_data.col_values(8)
        group_column_data = title_data.col_values(9)
        comment_column_data = title_data.col_values(10)

        current_day = ''
        lesson_num = ''

        for string_id in range(len(teacher_column_data)):

            if len(days_column_data[string_id]) != 0:
                current_day = days_column_data[string_id].lower()
                current_day = current_day.split()[0]

            if len(lesson_num_column_data[string_id]) != 0:
                lesson_num = lesson_num_column_data[string_id]

            if teachers_name in teacher_column_data[string_id].lower():
                comment = comment_column_data[string_id] if string_id < len(
                    comment_column_data) else ''
                info = [lesson_num,
                        subject_column_data[string_id],
                        classroom_column_data[string_id],
                        group_column_data[string_id],
                        comment]

                if title in titles_data.keys():
                    if current_day in titles_data[title].keys():
                        titles_data[title][current_day].append(info)
                    else:
                        titles_data[title][current_day] = [info]
                else:
                    titles_data[title] = {f'{current_day}': [info]}
    return titles_data


def make_person_schedule(teachers_name, time):
    data = {}
    good_titles = get_sheet_titles(time)
    if good_titles is None:
        return data, False, True, 0
    data = make_precursors(good_titles[0], teachers_name.lower())
    if data == {}:
        return data, True, False, 0
    return data, False, False, good_titles[1]