from view import *
from db_manipulation import get_all_month, insert_shedule_to_database, connect_database
from art import tprint
from simple_term_menu import TerminalMenu



def main():
    tprint("BIA-Technologies")
    # conn = 
    if connect_database() is None:
        print(Fore.RED + "Невозможно подключиться к базе данных!!!")
        return 0
    month_list = [i[0] for i in get_all_month()]
    print("Выберите месяц для составления расписания:")
    terminal_menu_month = TerminalMenu(month_list)
    index = terminal_menu_month.show()
    current_month = month_list[index]
    print(f"Вы выбрали {current_month}!")
    
    argument = ['yes', 'no']
    terminal_menu_add_database = TerminalMenu(argument)
    print("Хотите добавить расписание в базу данных?")
    index = terminal_menu_add_database.show()
    add_to_database = argument[index]
    if current_month in month_list:
        shedule_dict = create_shedule(current_month)   # Create shedule dict
        write_jsonfile(shedule_dict, file_name='shedule')  # write shedule to a json file
        shedule_frame = dataframe_shedule(shedule_dict)
        try:
            shedule_frame.to_csv('shedule.csv')
            print(Fore.GREEN + 'Расписание добавлено в файл shedule.csv')
        except Exception as error:
            print(Fore.RED + f"Не удалось записать расписание а файл shedulr.csv: {error}")
        
        if add_to_database == 'yes':
            if insert_shedule_to_database(shedule_dict, current_month) == True:
                print(Fore.GREEN + "Расписание добавлено в базу данных.")
            else:
                print(Fore.RED + 'Невозможно добавить данные в базу данных')
    else:
        print(Fore.RED + 'Неполадки в системе(нет доступа к базе данных).')

if __name__ == '__main__':
    main()
    # print(shedule_frame)






# json_frame = json.dumps(shedule).encode('utf-8')










