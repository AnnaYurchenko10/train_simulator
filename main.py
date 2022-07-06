import datetime
import json
from arrow import Arrow
from entrepot import Entrepot
from location_status import Location_Status
from terminal import Terminal
from train import Train
from train_status import Train_Status

RADUZNIY_POINT = 2500
ZVEZDA_POINT = 4000

year = 2021
start_month = 11
day = 1
hour = 00
end_month = 12
start_time = datetime.datetime(year, start_month, day, hour)
end_time = datetime.datetime(year, end_month, day, hour)

def init():

    global raduzniy
    global zvezda
    global polarniy
    global raduzniy_trains
    global zvezda_trains
    global trains

    raduzniy = Terminal(6000, 0, True)
    zvezda = Terminal(5000, 0, True)
    polarniy = Entrepot(0, 300, 200,15000)

    with open('DataTrains.json') as file_data_trains:
        data_train = json.load(file_data_trains)

    trains = [Train(**train) for train in data_train]
    raduzniy_trains = [train for train in trains if train.owner == 'raduzniy']
    zvezda_trains = [train for train in trains if train.owner == 'zvezda']

init()

for i in Arrow.range('hours', start_time, end_time):
    # добыча
    Terminal.production(raduzniy, 150, 10)
    # очередь из поездов
    queue_raduzniy_trains = []
    # заполнение очереди из поездов, движение поездов\
    Train.traffic(raduzniy_trains, queue_raduzniy_trains, Location_Status.TERMINAL_R.value, RADUZNIY_POINT)
    # проверка занятости пути
    if(raduzniy.is_free == True):
        global raduzniy_train
        if(len(queue_raduzniy_trains) > 0):
            raduzniy_train = queue_raduzniy_trains.pop(0)
            raduzniy_train.status = Train_Status.LOADING.value
            raduzniy_train.speed = raduzniy_train.speed - 5
            raduzniy.is_free = False
    # погрузка нефти
    Terminal.loading(raduzniy_train, 200, raduzniy)

    # if (raduzniy_train.cargo == raduzniy_train.capacity) and (raduzniy_train.distance_traveled != 0) or (raduzniy_train.status == Train_Status.WAIT.value):
    #     print("{}, {}, {}, {}, {}".format(i, raduzniy.oil, raduzniy.production, None, None))
    # else:
    #     print("{}, {}, {}, {}, {}, {}, {}".format(i, raduzniy.oil, raduzniy.production, raduzniy_train.name, raduzniy_train.cargo, raduzniy_train.status, raduzniy_train.distance_traveled))

    # добыча
    Terminal.production(zvezda, 50, 2)
    # очередь из поездов
    queue_zvezda_trains = []
    # заполнение очереди из поездов, движение поездов
    Train.traffic(zvezda_trains, queue_zvezda_trains, Location_Status.TERMINAL_Z.value, ZVEZDA_POINT)
    # проверка занятости пути
    if(zvezda.is_free == True):
        global zvezda_train
        if(len(queue_zvezda_trains) > 0):
            zvezda_train = queue_zvezda_trains.pop(0)
            zvezda_train.status = Train_Status.LOADING.value
            zvezda_train.speed -= 5
            zvezda.is_free = False
    # погрузка нефти
    Terminal.loading(zvezda_train, 250, zvezda)

    # if (zvezda_train.cargo == zvezda_train.capacity) and (zvezda_train.distance_traveled != 0) or (zvezda_train.status == Train_Status.WAIT.value):
    #    print("{}, {}, {}, {}, {}".format(i, zvezda.oil, zvezda.production, None, None))
    # else:
    #    print("{}, {}, {}, {}, {}, {}, {}".format(i, zvezda.oil, zvezda.production, zvezda_train.name, zvezda_train.cargo, zvezda_train.status, zvezda_train.distance_traveled))

# for train in trains:
#     print("{}, {}, {}, {}".format(train.name, train.status, train.location, train.distance_traveled))


    queue_polarniy_trains = []
    Entrepot.unloading_queue_trains(queue_polarniy_trains, trains)
    Entrepot.update_places(queue_polarniy_trains, polarniy)
    print("{}, {}, {}".format(i, polarniy.oil, Train.getNames(polarniy.trains)))
    Entrepot.loading_unloading_process(polarniy)

    train_loading = Entrepot.loading_place(polarniy)