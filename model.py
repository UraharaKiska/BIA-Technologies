import psycopg2
from config import *
import sqlalchemy as db 
from sqlalchemy.orm import DeclarativeBase





def connect_database():
    conn = None
    try:
        conn =  psycopg2.connect(
                                host = HOST,
                                database = DB_NAME,
                                user = LOGIN,
                                password = PASS,
                                )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn

def close_connection(conn):
    try:
        conn.close()
        print('Database connection closed')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


class Base(DeclarativeBase):
    pass


def create_tables():
    commands = ()