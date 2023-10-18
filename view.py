import json
import copy
import pandas as pd
from db_manipulation import get_first_weekday, get_name_from_database
from colorama import init
init()
from colorama import Fore, Back


MAX_HOURE = 144
WORKER_COUNT = 10  # количество работников
WEEKDAYS = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']     # дни недели
HARD_DAY = 'пн'
LITE_DAY = 'вс'

def write_jsonfile(data, file_name):
    try:
        with open(f"{file_name}.json", 'w', encoding='utf-8') as f:
            json_data = json.dump(data, f, ensure_ascii=False, indent=4)
            print(Fore.GREEN + f'Расписание добавлено в файл {file_name}.json.')
    except Exception as error:
        print(error)

def read_json(file_name):
    try:
         with open(f"{file_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as error:
        print(error)
    
def check_worker_hour(shedule):    # подсчет количества часов для каждого работника
    check = {}
    for i, j in shedule.items():
        for id, status in j['workers_status'].items():
            if id not in check:
                check[id] = 0
            if status == 'р':
                check[id] += 12
    return check


def check_worker_on_day(shedule):
    result = {}
    for key, value in shedule.items():
        count = 0
        for i in value['workers_status'].values():
            if i == 'р':
                count += 1
        sublist = {}
        sublist['weekday'] = value['weekday']
        sublist['count'] = count
        result[key] = sublist
    return  result


def dataframe_shedule(shedule_dict):
    days_frame = pd.DataFrame(shedule_dict, index=['weekday'])
    worker_frame = pd.DataFrame([i['workers_status'] for i in shedule_dict.values()])
    worker_frame = worker_frame.T
    worker_frame.columns += 1
    shedule_frame = pd.concat([days_frame, worker_frame], sort=False, axis=0)  # concatenate two frames
    shedule_frame.rename(index={'weekday': 'Сотрудники'}, inplace=True)
    return shedule_frame



def create_shedule(current_month):
    day_count,  first_weekday = get_first_weekday(current_month)               # количество дней в месяце(входной параметр)
    workers_name = get_name_from_database()                     # получения списка работников из базы данных
    shedule = {}                                                # будущий график работы
    offset = WEEKDAYS.index(first_weekday)                      # смещение первого дня месяца относительно понедельника
    hour_in_month = {}                                          # количество часов в месяце для каждого работника
    workers_status = {}                                         # статус работника: работает, выходной и тд.
    for i in range(1, day_count + 1 ):                          # проходимся по каждоиу дню в месяце
        shedule[i] = {}                                         # наш график будет содержать информацию о дне недели, и статус каждого рпботника
        shedule[i]['weekday'] = WEEKDAYS[(i + offset - 1) - \
                                (i + offset - 1) // 7 * 7]      # просчитываем текущий день недели
        offset_worker = WORKER_COUNT // 3                       # параметр для алгоритма расчета графика работы
        if shedule[i]['weekday'] == HARD_DAY:                       # если в понедельник, то необходимо усиление, для этого уменьшаем аргумент
            offset_worker = WORKER_COUNT // 5
        elif shedule[i]['weekday'] == LITE_DAY:
            offset_worker = WORKER_COUNT // 2                   # уменшаем колтичество работников, для этого повышаем аргумент
        first_worker_offset = (i - 1) - (i - 1) // offset_worker * offset_worker  # 3 возможных смещений: 0, 1, 2 для графика 1/2
        current_worker = 0   #
        worker_on_work = 0 + first_worker_offset                # номер работника, который должен выйти на работу
        while current_worker < len(workers_name):
            if current_worker == worker_on_work:                # если номер итерации совпал с номером работника, который должен выйти на работу, отмечаем в графике 'р'
                workers_status[workers_name[worker_on_work]] = 'р'
                if current_worker not in hour_in_month:
                    hour_in_month[current_worker] = 0
                hour_in_month[current_worker] += 12             # добавляем часы работнику
                worker_on_work += offset_worker                 # итерируемся к следуещему работнику, которому необходимо выйти на работу
            else:
                workers_status[workers_name[current_worker]] = 'в'
            current_worker += 1

        shedule[i]['workers_status'] = copy.deepcopy(workers_status)    # добавляем статусы о работниках в график

    return shedule




