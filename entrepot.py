class Entrepot(object):

    def __init__(self, oil, loading, unloading):
        self.oil = oil
        self.trains = [None] * 3
        self.loading = loading
        self.unloading = unloading
