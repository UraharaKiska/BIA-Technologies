import model
import json
import copy
import pandas

# if __name__ == "__main__":
#     conn = model.connect_database()
#     model.close_connection(conn)


def check_worker_hour(shedule):    # подсчет количества часов для каждого работника
    check = {}
    for i, j in shedule.items():
        for id, status in j['workers_status'].items():
            if id not in check:
                check[id] = 0
            if status == 'hui':
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


def write_jsonfile(shedule):
    try:
        with open("data.json", 'w', encoding='utf-8') as f:
            json_data = json.dump(shedule, f, ensure_ascii=False, indent=4)
    except Exception as error:
        print(error)


day_count = 30          # количество дней в месяце(входной параметр)
worker_count = 10       # количество работников
max_hour = 144          # максимальное количестов рабочих часов для каждого работника
week_days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']     # дни недели
shedule = {}            # будущий график работы
first_day = 'вс'        # день недели, с которго начинается текущий месяц
offset = week_days.index(first_day)     # смещение первого дня месяца относительно понедельника
hour_in_month = {}      # количество часов в месяце для каждого работника
workers_status = {}     # статус работника: работает, выходной и тд.
for i in range(1, worker_count + 1):     # иницализируем словарь статуса работников
    workers_status[i] = 'в'      # по дефолту у всех выходной
# [(current_day - 1 + offset) - (current_day - 1 + offset) // 7 * 7]
for i in range(1, day_count + 1 ):         # проходимся по каждоиу дню в месяце
    shedule[i] = {}                        # наш график будет содержать информацию о дне недели, и статус каждого рпботника
    shedule[i]['weekday'] = week_days[(i + offset - 1) - (i + offset - 1) // 7 * 7]  # просчитываем текущий день недели
    offset_worker = worker_count // 3       # параметр для алгоритма расчета графика работы
    if shedule[i]['weekday'] == 'пн':     # если в понедельник, то необходимо усиление, для этого уменьшаем аргумент
        offset_worker = worker_count // 5
    elif shedule[i]['weekday'] == 'вс':
        offset_worker = worker_count // 2  # уменшаем колтичество работников, для этого повышаем аргумент
    first_worker_offset = (i - 1) - (i - 1) // offset_worker * offset_worker  # 3 возможных смещений: 0, 1, 2 для графика 1/2
    current_worker = 1   #
    worker_on_work = 1 + first_worker_offset            # номер работника, который должен выйти на работу
    while current_worker <= worker_count:
        if current_worker == worker_on_work:            # если номер итерации совпал с номером работника, который должен выйти на работу, отмечаем в графике 'р'
            workers_status[worker_on_work] = 'р'
            if current_worker not in hour_in_month:
                hour_in_month[current_worker] = 0
            hour_in_month[current_worker] += 12        # добавляем часы работнику
            worker_on_work += offset_worker            # итериремся к следуещему работнику, которому необходимо выйти на работу
        else:
            workers_status[current_worker] = 'в'
        current_worker += 1

    shedule[i]['workers_status'] = copy.deepcopy(workers_status)    # добавляем статусы о работниках в график



# json_frame = json.dumps(shedule).encode('utf-8')










