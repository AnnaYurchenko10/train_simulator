import json

from location_status import Location_Status
from train_status import Train_Status

with open('DataEntrepot.json') as file_data:
    data = json.load(file_data)

LOADING_SPEED_POLARNIY = data['loading_speed']

class Train(object):

    def __init__(self, owner=None, name='loading_train', capacity=None, cargo=None, speed=None, status="loading", location=None, distance_traveled=None):
        self.owner = owner
        self.name = name
        self.capacity = capacity
        self.cargo = cargo
        self.speed = speed
        self.status = status
        self.location = location
        self.distance_traveled = distance_traveled
        self.loading = LOADING_SPEED_POLARNIY

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

    def getName(self):
        return self.name if self.name is not None else None

    def getNameByNumber(trains, number):
        return trains[number].name if trains[number] is not None else None

    def getCargo(trains, number):
        return trains[number].cargo if trains[number] is not None else 0