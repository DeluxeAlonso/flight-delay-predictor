class Weather:
    def __init__(self, wban, date, max_temp, min_temp, avg_temp,
                 snowfall, water, pressure, avg_speed, code_sum=''):
        self.wban = wban
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.avg_temp = avg_temp
        self.snowfall = snowfall
        self.water = water
        self.pressure = pressure
        self.avg_speed = avg_speed
        self.code_sum = self.process_code_sum(code_sum)
        self.rain = self.process_rain_code(self.code_sum)
        self.thunderstorm = self.process_thunderstorm_code(self.code_sum)
        self.snow = self.process_snow_code(self.code_sum)
        self.fog = self.process_fog_code(self.code_sum)
        self.mist = self.process_mist_code(self.code_sum)
        self.freezing = self.process_freezing_code(self.code_sum)

    def get_properties_array(self):
        return [self.wban, self.date, self.min_temp, self.avg_temp, self.max_temp, self.snowfall,
                self.water, self.pressure, self.avg_speed, self.code_sum]

    # DATASET CONSTRUCTION

    def get_properties_for_dataset(self):
        return [self.min_temp, self.avg_temp, self.max_temp, self.snowfall,
                self.water, self.pressure, self.avg_speed, self.rain, self.thunderstorm,
                self.snow, self.fog, self.mist, self.freezing]

    #RANDOM FOREST

    def get_properties_array_without_wban_date(self):
        return [self.min_temp, self.avg_temp, self.max_temp,
                self.water, self.pressure, self.avg_speed, self.rain, self.thunderstorm,
                self.snow, self.fog, self.mist, self.freezing]

    # NAIVE BAYES

    def get_categorical_properties(self):
        return [str(self.rain), str(self.thunderstorm), str(self.snow),
                str(self.fog), str(self.mist), str(self.freezing)]

    def get_numerical_properties(self):
        return [self.min_temp, self.avg_temp, self.max_temp, self.snowfall,
                self.water, self.pressure, self.avg_speed]

    def process_code_sum(self, code_sum):
        codes = []
        code_array = ' '.join(code_sum.split())
        code_array = code_array.split(' ')
        for i in range(len(code_array)):
            if len(code_array[i]) == 4:
                codes.append(code_array[i][:2])
                codes.append(code_array[i][2:4])
            else:
                codes.append(code_array[i])
        return ' '.join(codes)

    def process_rain_code(self,code_sum):
        code = ' '.join(code_sum.split())
        code_array = code.split(' ')
        if "RA" in code_array or "RA+" in code_array or "RA-" in code_array:
            return 1.0
        return 0.0

    def process_thunderstorm_code(self,code_sum):
        code = ' '.join(code_sum.split())
        code_array = code.split(' ')
        if "TS" in code_array or "TS+" in code_array or "TS-" in code_array:
            return 1.0
        return 0.0

    def process_snow_code(self,code_sum):
        code = ' '.join(code_sum.split())
        code_array = code.split(' ')
        if "SN" in code_array or "SN+" in code_array or "SN-" in code_array:
            return 1.0
        return 0.0

    def process_fog_code(self,code_sum):
        code = ' '.join(code_sum.split())
        code_array = code.split(' ')
        if "FG" in code_array or "FG+" in code_array or "FG-" in code_array:
            return 1.0
        return 0.0

    def process_mist_code(self, code_sum):
        code = ' '.join(code_sum.split())
        code_array = code.split(' ')
        if "BR" in code_array or "BR+" in code_array or "BR-" in code_array:
            return 1.0
        return 0.0

    def process_freezing_code(self, code_sum):
        code = ' '.join(code_sum.split())
        code_array = code.split(' ')
        if "FZ" in code_array or "FZ+" in code_array or "FZ-" in code_array:
            return 1.0
        return 0.0

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
        if min_temp == 'M' or min_temp.strip() == '':
            self._min_temp = None
        else:
            self._min_temp = float(min_temp)

    @property
    def max_temp(self):
        return self._max_temp

    @max_temp.setter
    def max_temp(self, max_temp):
        if max_temp == 'M' or max_temp.strip() == '':
            self._max_temp = None
        else:
            self._max_temp = float(max_temp)

    @property
    def avg_temp(self):
        return self._avg_temp

    @avg_temp.setter
    def avg_temp(self, avg_temp):
        if avg_temp == 'M' or avg_temp.strip() == '':
            self._avg_temp = None
        else:
            self._avg_temp = float(avg_temp)

    @property
    def snowfall(self):
        return self._snowfall

    @snowfall.setter
    def snowfall(self, snowfall):
        if snowfall.strip() == 'M' or snowfall.strip() == '':
            self._snowfall = None
        elif snowfall.strip() == 'T':
            self._snowfall = 0.0
        else:
            self._snowfall = float(snowfall)

    @property
    def water(self):
        return self._water

    @water.setter
    def water(self, water):
        if water.strip() == 'M' or water.strip() == '':
            self._water = None
        elif water.strip() == 'T':
            self._water = 0.0
        else:
            self._water = float(water)

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, pressure):
        if pressure == 'M' or pressure.strip() == '':
            self._pressure = None
        else:
            self._pressure = float(pressure)

    @property
    def avg_speed(self):
        return self._avg_speed

    @avg_speed.setter
    def avg_speed(self, avg_speed):
        if avg_speed == 'M' or avg_speed.strip() == '':
            self._avg_speed = None
        else:
            self._avg_speed = float(avg_speed)