import psycopg2
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

connection = psycopg2.connect(
    database = os.environ.get('DATABASE'),
    user = os.environ.get('USER'),
    password = os.environ.get('PASSWORD'),
    host = os.environ.get('HOST'),
    port = os.environ.get('PORT')
)

cursor = connection.cursor()

def init():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS raduzniy(
        date_and_time timestamp not null primary key,
        oil int not null,
        production int not null,
        train varchar(100),
        cargo int
    );
    CREATE TABLE IF NOT EXISTS zvezda(
        date_and_time timestamp not null primary key,
        oil int not null,
        production int not null,
        train varchar(100),
        cargo int
    );
    CREATE TABLE IF NOT EXISTS polarniy(
        date_and_time timestamp not null primary key,
        oil int not null,
        train_1 varchar(100),
        cargo_1 int,
        train_2 varchar(100),
        cargo_2 int,
        train_3 varchar(100),
        cargo_3 int
    );
    DELETE FROM raduzniy;
    DELETE FROM zvezda;
    DELETE FROM polarniy;''')

    connection.commit()

def insert_raduzniy_record(date_and_time, oil, production, train, cargo):
    cursor.execute('''
        INSERT INTO raduzniy (date_and_time, oil, production, train, cargo) values
        ('{}', {}, {}, '{}', {})'''.format(date_and_time, oil, production, train, cargo))
    connection.commit()

def insert_zvezda_record(date_and_time, oil, production, train, cargo):
    cursor.execute('''
        INSERT INTO zvezda (date_and_time, oil, production, train, cargo) values
        ('{}', {}, {}, '{}', {})'''.format(date_and_time, oil, production, train, cargo))
    connection.commit()

def insert_polarniy_record(date_and_time, oil, train_1, cargo_1, train_2, cargo_2, train_3, cargo_3):
    cursor.execute('''
           INSERT INTO polarniy (date_and_time, oil, train_1, cargo_1, train_2, cargo_2, train_3, cargo_3) values
           ('{}', {}, '{}', {}, '{}', {}, '{}', {})'''.format(date_and_time, oil, train_1, cargo_1, train_2, cargo_2, train_3, cargo_3))
    connection.commit()