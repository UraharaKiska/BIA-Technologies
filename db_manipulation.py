from models import *
import psycopg2

def connect_database():
    try:
        engine = db.create_engine(f"postgresql://{LOGIN}:{PASS}@{HOST}/{DB_NAME}")
        connection  = engine.connect()
        return connection
    except (db.exc.OperationalError, psycopg2.OperationalError) as error:
        return None
    
       




def get_name_from_database():    # функция для получения работников из базы данных
    engine = connect_database()
    workers_name = []
    with Session(autoflush=False, bind=engine) as session:
        user = session.query(Workers)
        for i in user:
            workers_name.append(i.name)
    return workers_name

def get_first_weekday(month):       # получение первого дня недели месяца
    engine = connect_database()
    try:
        with Session(autoflush=False, bind=engine) as session:
            data = session.query(Month.id, Month.days_count, Weekday.short_name).filter_by(name=month).join(Weekday)[0]
            return data[1], data[2]
    except Exception as error:
        print(f"In 'get_first_weekday'{error}")


def get_all_month():
    engine = connect_database()
    try:
        with Session(autoflush=False, bind=engine) as session:
            month = session.query(Month.name)
            return month
    except Exception as error:
        print(f"Error in 'get_all_month':{error}")


def insert_shedule_to_database(shedule, current_month):
    engine = connect_database()
    if engine is None:
        return False
    else:
        try:
            with Session(autoflush=False, bind=engine) as session:
                weekdays_data = session.query(Weekday.short_name, Weekday.id)
                workers_data = session.query(Workers)
                status_data = session.query(WorkerStatus)
                current_month_id = session.query(Month.id).filter_by(name=current_month)
                session.query(Shedule).filter(Shedule.month_id==current_month_id).delete()
                session.commit()
                weekdays_dict = {}
                workers_dict = {}
                status_dict = {}
                for i in workers_data:
                    workers_dict[i.name] = i.id 
                for i in weekdays_data:
                    weekdays_dict[i.short_name] = i.id
                # print(workers_dict)
                for i in status_data:
                    status_dict[i.short_name] = i.id
                for day, values in shedule.items():
                    # print(values)
                    for worker_name, status in values['workers_status'].items():
                        # print('hui')
                        insert = Shedule(current_month_id, day, weekdays_dict[values['weekday']], workers_dict[worker_name],status_dict[status])
                        session.add(insert)
                        session.commit()
                return True
        except exc.SQLAlchemyError as error:
            print(f'Не удалось добавить данные в базу данных: {error}')
