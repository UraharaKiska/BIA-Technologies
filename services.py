import psycopg2
from config import *
import sqlalchemy as db
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session, load_only


class Base(DeclarativeBase):
    pass


class Workers(Base):
    __tablename__ = "workers"

    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    name = db.Column("name", db.VARCHAR(100))
    name_unique = db.UniqueConstraint(name)

    def __init__(self, name):
        self.name = name

class WorkerStatus(Base):
    __tablename__ = "worker_status"
    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    short_name = db.Column('short_name', db.VARCHAR(20), nullable=False, unique=True)
    name = db.Column('name', db.VARCHAR(255), nullable=False, unique=True)
    
    def __init__(self, short_name, name):
        self.short_name = short_name
        self.name = name

class Weekday(Base):
    __tablename__ = "weekdays"
    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    short_name = db.Column('short_name', db.VARCHAR(20), nullable=False, unique=True)
    name = db.Column('name', db.VARCHAR(255), nullable=False, unique=True)
    
    def __init__(self, short_name, name):
        self.short_name = short_name
        self.name = name


class Month(Base):
    __tablename__ = "month"
    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    name = db.Column('name', db.VARCHAR(255), nullable=False, unique=True)
    first_weekday = db.Column('first_weekday', db.Integer, db.ForeignKey("weekdays.id", ondelete="CASCADE", onupdate="CASCADE"))
    
    def __init__(self, name, first_weekday):
        self.name = name
        self.first_weekday = first_weekday



class Shedule(Base):
    __tablename__ = "shedule"
    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    month = db.Column('month', db.Integer, db.ForeignKey("month.id", ondelete="CASCADE", onupdate="CASCADE"))
    day = db.Column('day', db.Integer)
    weekday = db.Column('weekday', db.Integer, db.ForeignKey("weekday.id", ondelete="CASCADE", onupdate="CASCADE"))
    worker_id = db.Column('worker_id', db.Integer, db.ForeignKey("workers.id", ondelete="CASCADE", onupdate="CASCADE"))
    worker_status = db.Column('worker_status', db.Integer, dp.ForeignKey("worker_status", ondelete="CASCADE", onupdate="CASCADE"))
    # time = db.Column('time')

    def __init__(self, month, day, weekday, worker_id, worker_status):
        self.month = month
        self.day = day
        self.weekday = weekday
        self.worker_id = worker_id
        self.worker_status = worker_status


def engine_database():
    engine = None
    try:
        engine = db.create_engine(f"postgresql://{LOGIN}:{PASS}@{HOST}/{DB_NAME}")
        print("Got sql engine")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return engine

def close_connection(conn):
    try:
        conn.close()
        print('Database connection closed')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)




# def create_tables():
#     commands = ()


# def main():
#     try:
#         engine = db.create_engine(f"postgresql://{LOGIN}:{PASS}@{HOST}/{DB_NAME}")
#         Base.metadata.create_all(bind=engine)
#         print('Bases created')
#     except Exception as ex:
#         print(ex)

# if __name__ == "__main__":
#     main()