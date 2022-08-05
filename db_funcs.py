import sqlite3


def get_data_from_db(db_name: str = 'conf.sqlite') -> tuple:
    """
        Функция подключается к существующей БД, либо создает файл БД в текущей директории. При отсутствии данных в БД,
        данные будут запрошены из консоли. Функция вернет кортеж со значениями в следующем порядке:
        (URL, API KEY, LANGUAGE)
    """

    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS data
            ( 
            URL TEXT, 
            API_KEY TEXT, 
            LANGUAGE TEXT
            )
    ''')

    cursor.execute('''
        SELECT * FROM data
    ''')

    if not cursor.fetchall():

        print('Для работы в данной программе, необходимо зарегистрироваться на сервисе https://dadata.ru/')
        print('После прохождения регистрации, в личном кабинете вам будут доступны ключ API и секретный ключ')
        print('Ключи можно найти по следующей ссылке: https://dadata.ru/profile/#info')
        print()

        url = 'https://dadata.ru/'
        api_key = input('Введите ваш API KEY: ').strip()
        language = input('Выберите желаемый язык для вывода заданного адреса. Введите \"ru\" или \"en\": ').strip()
        print()

        while language != 'ru' and language != 'en':
            print('Введено неверное обозначение языка вывода.')
            language = input('Введите \"ru\" - для выбора русского языка или \"en\" - для выбора английского языка: ')

        cursor.execute(f"INSERT INTO data (URL, API_KEY, LANGUAGE) VALUES (?, ?, ?)",
                       (url, api_key, language))

    cursor.execute('''
        SELECT * FROM data
    ''')

    result = cursor.fetchall()[0]
    connect.commit()
    connect.close()
    return result


def delete_data() -> None:
    """Функция удаляет информацию из таблицы БД"""
    connect = sqlite3.connect('conf.sqlite')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM data")
    connect.commit()
    connect.close()


def change_data() -> tuple:
    """Функция изменяет информацию в БД, в случае недействительного API KEY"""

    print('Введен недействительный API KEY, пожалуйста, убедитесь в правильности вводимого ключа.')
    print('API KEY можно найти по следующей ссылке: https://dadata.ru/profile/#info')
    delete_data()
    data = get_data_from_db()
    return data


if __name__ == '__main__':
    print(get_data_from_db())
    # delete_data()
