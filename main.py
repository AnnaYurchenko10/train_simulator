import datetime
import json

from arrow import Arrow

import db_helper
from entrepot import Entrepot
from location_status import Location_Status
from terminal import Terminal
from train import Train
from train_status import Train_Status

with open('DataConstants.json') as file_data_constants:
    data_constants = json.load(file_data_constants)

with open('DateTime.json') as file_date_time:
    date_time = json.load(file_date_time)

RADUZNIY_POINT = data_constants['raduzniy_point']
ZVEZDA_POINT = data_constants['zvezda_point']
EXPECTED_VALUE_RADUZNIY = data_constants['expected_value_raduzniy']
STANDARD_DEVIATION_RADUZNIY = data_constants['standard_deviation_raduzniy']
EXPECTED_VALUE_ZVEZDA = data_constants['expected_value_zvezda']
STANDARD_DEVIATION_ZVEZDA = data_constants['standard_deviation_zvezda']
SPEED_PERCENTAGE = data_constants['speed_percentage_1']
LOADING_SPEED_RADUZNIY = data_constants['loading_speed_raduzniy']
LOADING_SPEED_ZVEZDA = data_constants['loading_speed_zvezda']

year = date_time['year']
start_month = date_time['start_month']
day = date_time['day']
hour = date_time['hour']
end_month = date_time['end_month']
start_time = datetime.datetime(year, start_month, day, hour)
end_time = datetime.datetime(year, end_month, day, hour)

def init():

    global terminal
    global entrepot
    global raduzniy_trains
    global zvezda_trains
    global trains

    with open('DataTrains.json') as file_data_trains:
        data_train = json.load(file_data_trains)

    trains = [Train(**train) for train in data_train]
    raduzniy_trains = [train for train in trains if train.owner == 'raduzniy']
    zvezda_trains = [train for train in trains if train.owner == 'zvezda']

    with open('DataTerminal.json') as file_data_terminal:
        data_terminal = json.load(file_data_terminal)
    terminal = [Terminal(**terminal) for terminal in data_terminal]

    with open('DataEntrepot.json') as file_data_entrepot:
        data_entrepot = json.load(file_data_entrepot)
    entrepot = Entrepot(**data_entrepot)

def process(term, m, q, queue, trains, location_status, point):
    Terminal.production(term, m, q)
    # заполнение очереди из поездов, движение поездов
    Train.traffic(trains, queue, location_status, point)


init()
db_helper.init()

for i in Arrow.range('hours', start_time, end_time):
    for term in terminal:
        if(term.name == 'raduzniy'):
            queue_raduzniy_trains = []
            process(term, EXPECTED_VALUE_RADUZNIY, STANDARD_DEVIATION_RADUZNIY, queue_raduzniy_trains,raduzniy_trains, Location_Status.TERMINAL_R.value, RADUZNIY_POINT)
            # проверка занятости пути
            if(term.is_free == True):
                global raduzniy_train
                if(len(queue_raduzniy_trains) > 0):
                    raduzniy_train = queue_raduzniy_trains.pop(0)
                    raduzniy_train.status = Train_Status.LOADING.value
                    raduzniy_train.speed = raduzniy_train.speed * SPEED_PERCENTAGE
                    term.is_free = False
            # погрузка нефти
            Terminal.loading(raduzniy_train, LOADING_SPEED_RADUZNIY, term)
            # вывод расписания в базу данных
            if (raduzniy_train.status == Train_Status.LOADING.value) or (
                    (raduzniy_train.cargo == raduzniy_train.capacity) and (raduzniy_train.distance_traveled == 0)
                    and (raduzniy_train.status != Train_Status.WAIT.value)
            ):
                db_helper.insert_raduzniy_record(
                    i.strftime('%Y-%m-%d %H:%M:%S'), term.oil, term.production, Train.getName(raduzniy_train),
                    raduzniy_train.cargo
                )
            else:
                db_helper.insert_raduzniy_record(i.strftime('%Y-%m-%d %H:%M:%S'), term.oil, term.production, None, 0)

        if(term.name == 'zvezda'):
            # очередь из поездов
            queue_zvezda_trains = []
            process(term, EXPECTED_VALUE_ZVEZDA, STANDARD_DEVIATION_ZVEZDA, queue_zvezda_trains, zvezda_trains, Location_Status.TERMINAL_Z.value, ZVEZDA_POINT)
            # проверка занятости пути
            if(term.is_free == True):
                global zvezda_train
                if(len(queue_zvezda_trains) > 0):
                    zvezda_train = queue_zvezda_trains.pop(0)
                    zvezda_train.status = Train_Status.LOADING.value
                    zvezda_train.speed = zvezda_train.speed * SPEED_PERCENTAGE
                    term.is_free = False
            # погрузка нефти
            Terminal.loading(zvezda_train, LOADING_SPEED_ZVEZDA, term)

            # вывод расписания в базу данных
            if (zvezda_train.status == Train_Status.LOADING.value) or (
                    (zvezda_train.cargo == zvezda_train.capacity) and (zvezda_train.distance_traveled == 0)
                    and (zvezda_train.status != Train_Status.WAIT.value)
            ):
                db_helper.insert_zvezda_record(
                    i.strftime('%Y-%m-%d %H:%M:%S'), term.oil, term.production, Train.getName(zvezda_train),
                    zvezda_train.cargo
                )
            else:
                db_helper.insert_zvezda_record(i.strftime('%Y-%m-%d %H:%M:%S'), term.oil, term.production, None, 0)

        # очередь из поездов
    queue_polarniy_trains = []
    Entrepot.unloading_queue_trains(queue_polarniy_trains, trains)
    Entrepot.update_places(queue_polarniy_trains, entrepot)

    db_helper.insert_polarniy_record(
        i.strftime('%Y-%m-%d %H:%M:%S'), entrepot.oil,
        Train.getNameByNumber(entrepot.trains, 0), Train.getCargo(entrepot.trains, 0),
        Train.getNameByNumber(entrepot.trains, 1), Train.getCargo(entrepot.trains, 1),
        Train.getNameByNumber(entrepot.trains, 2), Train.getCargo(entrepot.trains, 2)
    )

    Entrepot.loading_unloading_process(entrepot)

    train_loading = Entrepot.loading_place(entrepot)