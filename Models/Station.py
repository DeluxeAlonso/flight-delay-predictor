class Station:
    def __init__(self, code, name, wban=None, latitude=None, longitude=None, timezone=None):
        self.code = str(code)
        self.name = str(name)
        self.wban = str(wban)
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone

    def get_properties_array(self):
        return [self.wban, self.name, self.longitude, self.longitude, self.timezone]