import csv
import json

def import_csv(path_to_import_csv_file): 
    data = [] # список словарей который получим при преобразовании       
    with open(path_to_import_csv_file, "r", newline='', encoding='UTF-8-sig') as file: 
        file_reader = csv.DictReader(file, delimiter = ";") 
        for row in file_reader:
            #row['contact_id'] = '' # Добавляем пустой ключ contact_id в словарь
            data.append(row)     
        for i in range(0, len(data)): 
            d1 = {'contact_id': ''}
            data[i], d1 = d1, data[i]
            data[i].update(d1)     

    return data 
    
def import_json(path_to_import_json_file):
    data = [] # список словарей который получим при преобразовании      
    with open(path_to_import_json_file, 'r', encoding='UTF-8') as file: #открываем файл на чтение
        data = json.load(file) #загружаем из файла данные в словарь data
        for i in range(0, len(data)): 
            d1 = {'contact_id': ''}
            data[i], d1 = d1, data[i]
            data[i].update(d1)
    return data


if __name__ == "__main__":
    from pprint import pprint
    path_to_import_json_file = 'import_phonebook.json'
    path_to_import_csv_file = 'import_phonebook.csv'

    
    print('******************csv_file******************')
    print(import_csv(path_to_import_csv_file), sort_dicts=False)
    
    print('******************json_file******************')
    print(import_json(path_to_import_json_file), sort_dicts=False)



  