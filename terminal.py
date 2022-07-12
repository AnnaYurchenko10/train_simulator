from location_status import Location_Status
from train_status import Train_Status
import numpy as numpy

class Terminal(object):

    def __init__(self, name, oil, production, is_free, expected_value, standard_deviation, loading_speed):
        self.name = name
        self.oil = oil
        self.production = production
        self.is_free = is_free
        self.expected_value = expected_value
        self.standard_deviation = standard_deviation
        self.loading_speed = loading_speed

    def loading(train, oil, terminal):
        if (train.cargo < train.capacity) and (terminal.oil >= oil) and (train.status == Train_Status.LOADING.value):
            train.cargo += oil
            terminal.oil -= oil
            if(train.cargo == train.capacity):
                terminal.is_free=True
                train.status = Train_Status.TRANSIT_IN_ENTREPOT.value
                train.location = Location_Status.IN_TRANSIT.value
                train = None
    
    def production(terminal):
        terminal.production = round(numpy.random.normal(terminal.expected_value, terminal.standard_deviation, None))
        terminal.oil += terminal.production
