import datetime
import numpy as numpy
import json
from arrow import Arrow
from location_status import Location_Status
from terminal import Terminal
from train import Train
from train_status import Train_Status

BIG_CAPACITY = 6000
MIDDLE_CAPACITY = 5000
LITTLE_CAPACITY = 4000

RADUZNIY_POINT = 2500
ZVEZDA_POINT = 4000

year = 2021
start_month = 11
day = 1
hour = 00
end_month = 12
start_time = datetime.datetime(year, start_month, day, hour)
end_time = datetime.datetime(year, end_month, day, hour)

# ПРИ ВЫГРУЗКЕ ДОБАВИТЬ 5 К СКОРОСТИ
def init():

    global raduzniy
    global zvezda
    global polarniy
    global raduzniy_trains
    global zvezda_trains

    raduzniy = Terminal(6000, 0, True)
    zvezda = Terminal(5000, 0, True)
    raduzniy_trains = []
    zvezda_trains = []

    with open('DataTrains.json') as file_data_trains:
        data_train = json.load(file_data_trains)

    trains = [Train(**train) for train in data_train]

    raduzniy_trains = [train for train in trains if train.owner == 'raduzniy']

    zvezda_trains = [train for train in trains if train.owner == 'zvezda']


    # raduzniy_trains = [
    #     Train('raduzniy_train_big_1', BIG_CAPACITY, 0, 35, Train_Status.WAIT.value, Location_Status.TERMINAL_R.value, 0),
    #     Train('raduzniy_train_big_2', BIG_CAPACITY, 0, 35, Train_Status.WAIT.value, Location_Status.TERMINAL_R.value, 0),
    #     Train('raduzniy_train_little_3', LITTLE_CAPACITY, 4000, 40, Train_Status.TRANSIT_IN_ENTREPOT.value, Location_Status.IN_TRANSIT.value, 1750),
    #     Train('raduzniy_train_little_4', LITTLE_CAPACITY, 0, 40, Train_Status.TRANSIT_IN_TERMINAL.value, Location_Status.IN_TRANSIT.value, 2500),
    #     Train('raduzniy_train_little_5', LITTLE_CAPACITY, 4000, 40, Train_Status.WAIT.value, Location_Status.ENTREPOT_P.value, 2500)
    # ]


    # zvezda_trains = [
    #     Train('zvezda_train_1', MIDDLE_CAPACITY, 0, 45, Train_Status.WAIT.value, Location_Status.TERMINAL_Z.value, 0),
    #     Train('zvezda_train_2', MIDDLE_CAPACITY, 0, 45, Train_Status.WAIT.value, Location_Status.TERMINAL_Z.value, 0)
    # ]

    # polarniy = Polarniy(0, 300, 200)

def loading(train, oil, terminal):
    if (train.cargo < train.capacity) and (terminal.oil >= oil):
        train.cargo += oil
        terminal.oil -= oil
        if(train.cargo == train.capacity):
            terminal.is_free=True
            train.status = Train_Status.TRANSIT_IN_ENTREPOT.value
            train.location = Location_Status.IN_TRANSIT.value

def production(terminal, loc, scale):
    terminal.production = round(numpy.random.normal(loc, scale, None))
    terminal.oil += terminal.production

def traffic(trains, queue_trains, terminal_name, terminal_point):
    for train in trains:
        if(train.status == Train_Status.WAIT.value) and (train not in queue_trains) and (train.location == terminal_name):
            queue_trains.append(train)
        if(train.location == Location_Status.IN_TRANSIT.value) and (train.distance_traveled < terminal_point):
            train.distance_traveled += train.speed
        elif(train.status == Train_Status.TRANSIT_IN_ENTREPOT.value) and (train.distance_traveled >= terminal_point):
            train.status = Train_Status.WAIT.value
            train.location = Location_Status.ENTREPOT_P.value
            train.distance_traveled = 0
        elif (train.status == Train_Status.TRANSIT_IN_TERMINAL.value) and (train.distance_traveled >= terminal_point):
            train.status = Train_Status.WAIT.value
            train.location = terminal_name
            train.distance_traveled = 0

init()

for i in Arrow.range('hours', start_time, end_time):
    # добыча
    production(raduzniy, 150, 10)
    # очередь из поездов
    queue_raduzniy_trains = []
    # заполнение очереди из поездов, движение поездов\
    traffic(raduzniy_trains, queue_raduzniy_trains, Location_Status.TERMINAL_R.value, RADUZNIY_POINT)
    # проверка занятости пути
    if(raduzniy.is_free == True):
        global raduzniy_train
        if(len(queue_raduzniy_trains) > 0):
            raduzniy_train = queue_raduzniy_trains.pop(0)
            raduzniy_train.status = Train_Status.LOADING.value
            raduzniy_train.speed = raduzniy_train.speed - 5
            raduzniy.is_free = False
    # погрузка нефти
    loading(raduzniy_train, 200, raduzniy)

    if (raduzniy_train.cargo == raduzniy_train.capacity) and (raduzniy_train.distance_traveled != 0) or (raduzniy_train.status == Train_Status.WAIT.value):
        print("{}, {}, {}, {}, {}".format(i, raduzniy.oil, raduzniy.production, None, None))
    else:
        print("{}, {}, {}, {}, {}, {}, {}".format(i, raduzniy.oil, raduzniy.production, raduzniy_train.name, raduzniy_train.cargo, raduzniy_train.status, raduzniy_train.distance_traveled))

    # добыча
    production(zvezda, 50, 2)
    # очередь из поездов
    queue_zvezda_trains = []
    # заполнение очереди из поездов, движение поездов
    traffic(zvezda_trains, queue_zvezda_trains, Location_Status.TERMINAL_Z.value, ZVEZDA_POINT)
    # проверка занятости пути
    if(zvezda.is_free == True):
        global zvezda_train
        if(len(queue_zvezda_trains) > 0):
            zvezda_train = queue_zvezda_trains.pop(0)
            zvezda_train.status = Train_Status.LOADING.value
            zvezda_train.speed = zvezda_train.speed - 5
            zvezda.is_free = False
    # погрузка нефти
    loading(zvezda_train, 250, zvezda)

    # if (zvezda_train.cargo == zvezda_train.capacity) and (zvezda_train.distance_traveled != 0) or (zvezda_train.status == Train_Status.WAIT.value):
    #    print("{}, {}, {}, {}, {}".format(i, zvezda.oil, zvezda.production, None, None))
    # else:
    #    print("{}, {}, {}, {}, {}, {}, {}".format(i, zvezda.oil, zvezda.production, zvezda_train.name, zvezda_train.cargo, zvezda_train.status, zvezda_train.distance_traveled))

for train in raduzniy_trains:
    print("{}, {}, {}, {}".format(train.name, train.status, train.location, train.distance_traveled))
