import http
import httpx
from time import sleep

import db_funcs
import dadata_funcs


if __name__ == '__main__':

    data = db_funcs.get_data_from_db()

    print('Добро пожаловать!')
    print('Данная программа поможет вам определить географические координаты по адресу')
    print()

    while True:
        try:
            res = dadata_funcs.define_cords(data)
            if res == 'end':
                break
        except httpx.HTTPStatusError:
            if http.HTTPStatus.FORBIDDEN == 403:
                data = db_funcs.change_data()

    print('\n\nБлагодарим за использование нашего сервиса. Будем рады видеть вас снова!\n\n')
    sleep(3)
