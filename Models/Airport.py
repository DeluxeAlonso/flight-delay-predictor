import Utils
from Models.Station import Station

class Airport(Station):
    def has_location(self):
        if self.longitude and self.longitude:
            return True
        else:
            return False