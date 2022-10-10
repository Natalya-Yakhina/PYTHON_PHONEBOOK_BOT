from database_module import get_all_contacts
import csv

def export_csv():
    temp = get_all_contacts() # возвращает весь справочник из рабочего файла

    file_csv = "bd_csv_export.csv" # файл в который выгружаем

    with open(file_csv,"w", encoding='UTF-8', newline="") as file: 
        colone = temp[0].keys()
        writer = csv.DictWriter(file, fieldnames=colone)
        writer.writeheader()
        writer.writerows(temp)
    
    print(f"данные перенесены в файл {file_csv}")

    return file_csv
