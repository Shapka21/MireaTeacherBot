import sqlite3


def check_in_data(user_id):
    con = sqlite3.connect("data.db")
    cursor = con.cursor()
    query = "SELECT telegram_id FROM teacher_test WHERE telegram_id=?;"
    params = (user_id,)
    res = cursor.execute(query, params).fetchone()
    con.close()
    if bool(res):
        return True
    return False


async def make_user_profile(user_id):
    con = sqlite3.connect("data.db")
    cursor = con.cursor()
    query = "INSERT INTO teacher_test (telegram_id) VALUES (?)"
    params = (user_id,)
    cursor.execute(query, params)
    con.commit()
    con.close()


def get_user_info_name(user_id):
    con = sqlite3.connect("data.db")
    cursor = con.cursor()
    query = "SELECT name_teacher FROM teacher_test WHERE telegram_id=?"
    params = (user_id,)
    cursor.execute(query, params)
    result = cursor.fetchall()
    con.close()
    return result[0] if result else None


async def set_user_info_name(user_id, name):
    con = sqlite3.connect("data.db")
    cursor = con.cursor()
    query = "UPDATE teacher_test SET name_teacher=? WHERE telegram_id=?"
    params = (name, user_id)
    cursor.execute(query, params)
    con.commit()
    cursor.close()


# def drop_info_in_table():
#     con = sqlite3.connect("../data.db")
#     cursor = con.cursor()
#     query = "DROP TABLE teacher_test;"
#     cursor.execute(query)
#     query = "CREATE TABLE teacher_test(telegram_id text, name_teacher text);"
#     cursor.execute(query)
#     con.commit()
#     cursor.close()
#
# drop_info_in_table()
