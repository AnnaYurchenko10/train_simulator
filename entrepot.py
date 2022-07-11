import json

from location_status import Location_Status
from train_status import Train_Status
from train import Train

with open('DataConstants.json') as file_data_constants:
    data_constants = json.load(file_data_constants)

ENTERPOT_CAPACITY = data_constants['enterpot_capacity']
SPEED_PERCENTAGE = data_constants['speed_percentage_2']
SIZE_LIST_POLARNIY = data_constants['size_list_polarniy']

class Entrepot(object):

    def __init__(self, oil, loading, unloading, max_capacity):
        self.oil = oil
        self.trains = [None] * SIZE_LIST_POLARNIY
        self.loading = loading
        self.unloading = unloading
        self.max_capacity = max_capacity
    
    def unloading_queue_trains(queue_trains, trains):
        for train in trains:
            if(train.status == Train_Status.WAIT.value) and (train not in queue_trains) and (train.location == Location_Status.ENTREPOT_P.value):
                queue_trains.append(train)

    def has_free_place(trains):
        index = 0
        for train in trains:
            if train is None:
                return index
            index += 1

    def update_places(queue_trains, entrepot):
        if len(queue_trains) > 0:
            free_place = Entrepot.has_free_place(entrepot.trains)
            if (entrepot.oil < ENTERPOT_CAPACITY) and (free_place is not None):
                current_train = queue_trains.pop(0)
                current_train.status = Train_Status.UNLOADING.value
                entrepot.trains[free_place] = current_train
            
    def loading_unloading_process(entrepot):
        index = 0
        for train in entrepot.trains:
            if train is not None:
                if(train.cargo > 0) and (entrepot.max_capacity > entrepot.oil) and (train.status == Train_Status.UNLOADING.value):
                    entrepot.oil += entrepot.unloading
                    train.cargo -= entrepot.unloading
                    if(train.cargo == 0):
                        train.status = Train_Status.TRANSIT_IN_TERMINAL.value
                        train.location = Location_Status.IN_TRANSIT.value
                        train.speed = train.speed * SPEED_PERCENTAGE
                        entrepot.trains[index] = None
                if (train.capacity != train.cargo) and (train.status == Train_Status.LOADING.value):
                    if (train.cargo + train.loading > train.capacity):
                        entrepot.oil = entrepot.oil - (train.capacity - train.cargo)
                        train.cargo = train.cargo + (train.capacity - train.cargo)
                    else:
                        train.cargo += train.loading
                        entrepot.oil -= train.loading
                    if (train.cargo == train.capacity):
                        entrepot.trains[index] = None
            index += 1

    def loading_place(entrepot):
        if(entrepot.oil >= ENTERPOT_CAPACITY):
            free_place = Entrepot.has_free_place(entrepot.trains)
            isFirst = True
            for train in entrepot.trains:
                if train is not None:
                    if (train.status == Train_Status.LOADING.value):
                        isFirst = False
                        if (free_place is not None) and ((entrepot.oil - (train.capacity - train.cargo)) > train.capacity):
                            entrepot.trains[free_place] = Train(capacity=ENTERPOT_CAPACITY, cargo=0)

            if isFirst and free_place is not None:
                entrepot.trains[free_place] = Train(capacity=ENTERPOT_CAPACITY, cargo=0)