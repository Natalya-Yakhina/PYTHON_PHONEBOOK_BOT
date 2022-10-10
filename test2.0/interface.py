import time
import art
from art import *  # библиотека для работы с ascii артом


def error_input():
    print('\033[5;31mОшибка!' + art("error"))
    print('\033[21mПожалуйста введите число, соответствующее пункту меню.')
    time.sleep(1)


def done_message():
    print('\033[5;32mВыполнено!' + art("cat4"))


main_menu = \
    'Выберите пункт меню:\n\
    1. /Start Список контактов\n\
    2. /show_cont Список контактов\n\
    3. Поиск контакта\n\
    4. Добавить контакт вручную\n\
    5. Изменить контакт\n\
    6. Импорт контактов\n\
    7. Экспорт контактов'


def show_contacts(data):  # 1 in menu
    if data != []:
        text =''
        #print('\033[4mСписок контактов:')
        for item in range(len(data)):
            a = data[item]['contact_id']
            b = data[item]['surname']
            c = data[item]['name']
            d = data[item]['phone']
            e = data[item]['comment']
            text += f'{a}) {b} {c}. {d}. {e}.\n'
        #print(50 * "•")
    else:
        text = 'Контакты не найдены'
    return text

def search_contact():
    search_request = input('Введите данные для поиска: ')
    print(50 * "=")
    return search_request


def add_contact():
    print('\033[3mДобавление контакта')
    print(50 * "-")
    contact_surname = input('Введите фамилию ')  # plain text
    contact_name = input('Введите имя ')  # DD-MM-YY
    contact_number = input('Введите номер телефона')
    commentary = input('Комментарий')
    contact = [{'contact_id': '', 'surname': contact_surname, 'name': contact_name, 'phone': contact_number,
                'comment': commentary}, ]
    return contact  # возвращение списка словаря


def change_contact():
    print('\033[4mИзменить контакт:')
    print(50 * "~")
    contact_id = input('Выберите контакт для внесения изменений:')
    return int(contact_id)


def change_contact_content(one_contact):
    while True:
        menu_command = input('Что необходимо сделать?1\n 1 - Изменить содержание \n 2 - Удалить контакт\n')
        if menu_command == '1':
            print('\033[4mИзменить содержание контакта:')
            while True:
                submenu_command = input(
                    'Что необходимо изменить?\n 1 - Изменить фамилию \n 2 - Изменить имя\n 3 - Изменить номер телефона\n 4 - Изменить комментарий\n')
                match submenu_command:
                    case '1':  # Изменить фамилию
                        print('Введите фамилию')
                        one_contact['surname'] = input()
                        done_message()
                        break
                    case '2':  # Изменить имя
                        print('Введите имя')
                        one_contact['name'] = input()
                        done_message()
                        break
                    case '3':  # Изменить номер телефона
                        print('Введите номер телефона')
                        one_contact['phone'] = input()
                        done_message()
                        break
                    case '4':  # Изменить комментарий
                        print('Введите комментарий')
                        one_contact['comment'] = input()
                        done_message()
                        break
                    case _:
                        error_input()
            break
        elif menu_command == '2':
            one_contact['comment'] = 'Я что-то нажал и всё сломалось'  # удаление по ID
            done_message()
            break
    return one_contact


def bye_mess():  # 6 in menu
    print('Работа завершена!')


def import_contacts():
    print('\033[4mИмпорт контактов:')
    print('Пожалуйста выберите формат файла для импорта:')
    import_type = input('csv\n json\n ')
    print('Пожалуйста введите имя файла для импорта:')
    import_name = input()
    import_data = [import_type, import_name]
    return import_data


def export_contacts():
    print('\033[4mЭкспорт контактов:')
    print('Пожалуйста выберите формат файла для экпорта:')
    export_type = input('csv\n json\n')
    print('Пожалуйста введите имя файла для экспорта:')
    export_name = input()
    export_data = [export_type, export_name]
    return export_data


def result_mess(done):
    if done:
        done_message()
    else:
        print('\033[5;31mПроизошла ошибка при выполнении операции!' + art("error"))