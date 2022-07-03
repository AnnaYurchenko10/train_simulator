from enum import Enum


class Train_Status(Enum):

    WAIT = "wait"
    TRANSIT_IN_TERMINAL = "transit_in_terminal"
    TRANSIT_IN_ENTREPOT = "transit_in_entrepot"
    LOADING = "loading"
    UNLOADING = "unloading"