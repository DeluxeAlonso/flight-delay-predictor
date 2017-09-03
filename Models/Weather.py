import Utils

class Weather:
    def __init__(self, wban, date, max_temp, min_temp, avg_temp,
                 snowfall, water, pressure, avg_speed):
        self.wban = wban
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.avg_temp = avg_temp
        self.snowfall = snowfall
        self.water = water
        self.pressure = pressure
        self.avg_speed = avg_speed

    def get_properties_array(self):
        return [self.wban, self.date, self.min_temp, self.avg_temp, self.max_temp, self.snowfall,
                self.water, self.pressure, self.avg_speed]

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        date = str(date)
        year, month, day = date[0:4], date[4:6], date[6:8]
        date = year + '-' + month + '-' + day
        self._date = date

    @property
    def min_temp(self):
        return self._min_temp

    @min_temp.setter
    def min_temp(self, min_temp):
        if min_temp == 'M':
            self._min_temp = None
        else:
            self._min_temp = min_temp

    @property
    def max_temp(self):
        return self._max_temp

    @max_temp.setter
    def max_temp(self, max_temp):
        if max_temp == 'M':
            self._max_temp = None
        else:
            self._max_temp = max_temp

    @property
    def avg_temp(self):
        return self._avg_temp

    @avg_temp.setter
    def avg_temp(self, avg_temp):
        if avg_temp == 'M':
            self._avg_temp = None
        else:
            self._avg_temp = avg_temp

    @property
    def snowfall(self):
        return self._snowfall

    @snowfall.setter
    def snowfall(self, snowfall):
        if snowfall.strip() == 'M':
            self._snowfall = None
        elif snowfall.strip() == 'T':
            self._snowfall = 0.0
        else:
            self._snowfall = snowfall

    @property
    def water(self):
        return self._water

    @water.setter
    def water(self, water):
        if water.strip() == 'M':
            self._water = None
        elif water.strip() == 'T':
            self._water = 0.0
        else:
            self._water = water

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, pressure):
        if pressure == 'M':
            self._pressure = None
        else:
            self._pressure = pressure

    @property
    def avg_speed(self):
        return self._avg_speed

    @avg_speed.setter
    def avg_speed(self, avg_speed):
        if avg_speed == 'M':
            self._avg_speed = None
        else:
            self._avg_speed = avg_speed