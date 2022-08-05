from typing import Optional

from dadata import Dadata


def clarify_address(dadata: Dadata, result: list, data: tuple) -> Optional[list, str]:
    """Функция позволяет пользователю выбрать один из подходящих адресов и создать новый запрос с уточненным адресом"""

    for i in range(1, len(result) + 1):
        print(f"({i}) - {result[i - 1]['unrestricted_value'].replace('()', '')}")
    print('\nВыберите подходящий вариант из списка. Если подходящий вариант отсутствует, введите 0')
    num_of_var = int(input('Введите порядковый номер: '))
    print()

    if num_of_var == 0:
        print('Попробуйте уточнить запрос. Введите искомый адрес в следующем формате: \"город\" \"улица\" \"дом\" ')
        print('Для выхода из программы введите \"exit\"')
        new_search = input('Введите новый адрес: ')
        if new_search == 'exit':
            return 'end'
        new_result = dadata.suggest("address", query=new_search, count=20, language=data[2])
    else:
        new_result = dadata.suggest("address", query=result[num_of_var - 1]['unrestricted_value'], count=20,
                                    language=data[2])

    if new_result == result:
        new_result = dadata.suggest("address", query=result[num_of_var - 1]['unrestricted_value'], count=1,
                                    language=data[2])
    return new_result


def define_cords(data: tuple) -> Optional[None, str]:
    """Функция определяет координаты запрашиваемого адреса"""

    token = data[1]
    language = data[2]

    with Dadata(token) as dadata:
        print('Для получения точных координат, введите искомый адрес (без кавычек)')
        print('Например: \"москва вавилова 19\"')
        print('Для выхода из программы введите \"exit\"')
        query = input('Введите адрес: ').strip()

        if query == 'exit':
            return 'end'

        result = dadata.suggest("address", query=query, count=20, language=language)

        while len(result) > 1:

            if int(result[0]['data']['fias_level']) >= 8:
                break

            result = clarify_address(dadata, result, data)

            if result == 'end':
                return 'end'

        if type(result) == list and result:
            result = result[0]

        if not result:
            print('\nПо вашему запросу не найдено ни одного адреса. Попробуйте ввести адрес в следующем формате:')
            print(r'"город улица дом"')
            return

        print('\n\n\n\n\n')
        print(f"Запрошенный адрес: {result['unrestricted_value']}")
        print('Координаты:')
        print(f"Широта - {result['data']['geo_lat']}")
        print(f"Долгота - {result['data']['geo_lon']}\n\n")