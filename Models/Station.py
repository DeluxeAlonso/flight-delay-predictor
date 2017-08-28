class Station:
    def __init__(self, code, name, latitude=None, longitude=None, timezone=None):
        self.code = str(code)
        self.name = str(name)
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone

    def get_properties_array(self):
        return [self.code, self.name, self.longitude, self.longitude, self.timezone]