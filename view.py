import json



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
    



