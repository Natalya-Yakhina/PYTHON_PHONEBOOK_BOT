# Процедуры работы с базой данных

import json

path_to_db = 'db_phonebook.json'

def get_all_contacts():  # возвращает весь список контактов из файла db_phonebook.json
    with open(path_to_db, 'r', encoding='UTF-8') as file:
        data = json.load(file)
        data = [data[i] for i in range(0, len(data))]
    return data

def get_one_contact(contact_id_get): # возвращает один контакт по его contact_id
    with open(path_to_db, 'r', encoding='UTF-8') as file: # читает данные из базы
        data = json.load(file)
        one_contact_get = {}
        for i in range(0, len(data)): 
            if contact_id_get == data[i]['contact_id']:
                one_contact_get = data[i]
                break
    return one_contact_get

def get_contact_info(contact_info_get): # возвращает контакты по вхождению в значение любого из ключей surname, name, phone, comment
    with open(path_to_db, 'r', encoding='UTF-8') as file: # читает данные из базы 
        data = json.load(file)
        info_contact_get = []

        for i in range(0, len(data)): 
            if  contact_info_get.lower() in data[i]['surname'].lower():
                info_contact_get.append(data[i])
            elif contact_info_get.lower() in data[i]['name'].lower():
                info_contact_get.append(data[i])
            elif contact_info_get.lower() in data[i]['phone'].lower():
                info_contact_get.append(data[i])
            elif contact_info_get.lower() in data[i]['comment'].lower():
                info_contact_get.append(data[i])
 
    return info_contact_get

def add_contacts(contacts_new_dict):  # добавление новых контактов в БД
                                                                        
    with open(path_to_db, 'r', encoding='UTF-8') as file: # читает данные из базы 
        data = json.load(file)            
        for i in range(0, len(contacts_new_dict)): 
            contacts_new_dict[i]['contact_id'] = data[len(data)-1]['contact_id'] + 1
            data.append(contacts_new_dict[i])     # добавляет в список словарей новый контакт   
    with open(path_to_db, 'w', encoding='UTF-8') as file: # записывает в базу данных обновленный список словарей
        json.dump(data, file, indent=4)

def change_contact(contact_edit):  # изменение контакта
    with open(path_to_db, 'r', encoding='UTF-8') as file: # читает данные из базы 
        data = json.load(file)

        for i in range(0, len(data)): # для изменения контакта c conroct_id = 6, находим в БД словарь с contact_id = 6 и перезаписываем его
            if contact_edit['contact_id'] == data[i]['contact_id']:
                data[i] = contact_edit
        
    with open(path_to_db, 'w', encoding='UTF-8') as file: # записывает в базу данных обновленный список словарей
        json.dump(data, file, indent=4)    

def delete_contact(contact_id_delete): # удаление контакта в БД по его id
    with open(path_to_db, 'r', encoding='UTF-8') as file: # читает данные из базы
        data = json.load(file)
                  
        for i in range(0, len(data)): 
            if data[i]['contact_id'] == contact_id_delete: # находит индекс элемента в списке словарей с нужным deal_id
                index_del = i
                break
        data.pop(index_del)   # удаляет из списка словарь с нужным contact_id
        for i in range(0, len(data)): # перезаписавает в каждом словаре списка ключ contact_id
            data[i]['contact_id'] = i+1
    with open(path_to_db, 'w', encoding='UTF-8') as file: # записывает в базу данных обновленный список словарей
        json.dump(data, file, indent=4)    

def clear_db(path_to_db): # очистка базы данных
    first_element = [{'id_counter': 0}, ]
    with open(path_to_db, 'w') as file:
        json.dump(first_element, file, indent=4)