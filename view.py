import json

month_dict = {'январь': {'days': 31, 'first_weekday': 'вс'},
              'февраль': {'days': 28, 'first_weekday': 'ср'},
              'март': {'days': 31, 'first_weekday': 'ср'},
              'апрель': {'days': 30, 'first_weekday': 'сб'},
              'май': {'days': 31, 'first_weekday': 'пн'},
              'июнь': {'days': 30, 'first_weekday': 'чт'},
              'июль': {'days': 31, 'first_weekday': 'сб'},
              'август': {'days': 31, 'first_weekday': 'вт'},
              'сентябрь': {'days': 30, 'first_weekday': 'пт'},
              'октябрь': {'days': 31, 'first_weekday': 'вс'},
              'ноябрь': {'days': 30, 'first_weekday': 'ср'},
              'декабрь': {'days': 31, 'first_weekday': 'пт'}
}


def write_jsonfile(data, file_name):
    try:
        with open(f"{file_name}.json", 'w', encoding='utf-8') as f:
            json_data = json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as error:
        print(error)

def read_json(file_name):
    try:
         with open(f"{file_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as error:
        print(error)
    



