import enum

class Location_Status(enum.Enum):
    TERMINAL_R = 'terminal_raduzniy'
    TERMINAL_Z = 'terminal_zvezda'
    ENTREPOT_P = 'entrepot_polarniy'
    IN_TRANSIT = 'in_transit'