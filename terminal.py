from location_status import Location_Status
from train_status import Train_Status
import numpy as numpy

class Terminal(object):

    def __init__(self, oil, production, is_free):
        self.oil = oil
        self.production = production
        self.is_free = is_free

    def loading(train, oil, terminal):
        if (train.cargo < train.capacity) and (terminal.oil >= oil) and (train.status == Train_Status.LOADING.value):
            train.cargo += oil
            terminal.oil -= oil
            if(train.cargo == train.capacity):
                terminal.is_free=True
                train.status = Train_Status.TRANSIT_IN_ENTREPOT.value
                train.location = Location_Status.IN_TRANSIT.value
    
    def production(terminal, loc, scale):
        terminal.production = round(numpy.random.normal(loc, scale, None))
        terminal.oil += terminal.production

