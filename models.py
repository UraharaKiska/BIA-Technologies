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
    first_weekday_id = db.Column('first_weekday_id', db.Integer, db.ForeignKey("weekdays.id", ondelete="CASCADE", onupdate="CASCADE"))
    days_count = db.Column('days_count', db.Integer)
    
    def __init__(self, name, first_weekday):
        self.name = name
        self.first_weekday = first_weekday



class Shedule(Base):
    __tablename__ = "shedule"
    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    month_id = db.Column('month_id', db.Integer, db.ForeignKey("month.id", ondelete="CASCADE", onupdate="CASCADE"))
    day = db.Column('day', db.Integer)
    weekday_id = db.Column('weekday_id', db.Integer, db.ForeignKey("weekdays.id", ondelete="CASCADE", onupdate="CASCADE"))
    worker_id = db.Column('worker_id', db.Integer, db.ForeignKey("workers.id", ondelete="CASCADE", onupdate="CASCADE"))
    worker_status_id = db.Column('worker_status_id', db.Integer, db.ForeignKey("worker_status.id", ondelete="CASCADE", onupdate="CASCADE"))
    # time = db.Column('time')

    def __init__(self, month_id, day, weekday, worker_id, worker_status_id):
        self.month_id = month_id
        self.day = day
        self.weekday_id = weekday
        self.worker_id = worker_id
        self.worker_status_id = worker_status_id


# class HourCount(Base):
#     __tablename__ = "hour_count"
#     id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
#     month_id = db.Column('month_id', db.Integer, db.ForeignKey("month.id", ondelete="CASCADE", onupdate="CASCADE"))
#     worker_id = db.Column('worker_id', db.Integer, db.ForeignKey("workers.id", ondelete="CASCADE", onupdate="CASCADE"))
#     hour = db.Column('hour', db.Integer)



def main():
    try:
        engine = db.create_engine(f"postgresql://{LOGIN}:{PASS}@{HOST}/{DB_NAME}")
        Base.metadata.create_all(bind=engine)
        print('Bases created')
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()