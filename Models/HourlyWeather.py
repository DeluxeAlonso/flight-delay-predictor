from datetime import datetime, timedelta

class HourlyWeather:
    def __init__(self, wban, date, time , temp, sky_condition, visibility, wind_speed, pressure,
                 humidity, altimeter):
        self.wban = wban
        self.date = date
        self.time = self.get_time_hour(time)
        self.temp = temp
        self.sky_condition = sky_condition
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.pressure = pressure
        self.humidity = humidity
        self.altimeter = altimeter

    def get_properties_array(self):
        return [self.wban, self.date, self.time, self.temp, self.sky_condition, self.visibility,
                self.wind_speed, self.pressure, self.humidity, self.altimeter, self.code_sum]

    # DATASET CONSTRUCTION
    def get_properties_for_dataset(self):
        return [self.temp, self.sky_condition, self.visibility, self.wind_speed,
                self.pressure, self.humidity, self.altimeter, self.rain, self.thunderstorm,
                self.snow, self.fog, self.mist, self.freezing]

    # RANDOM FOREST
    def get_properties_array_without_wban_date(self):
        return [self.temp, self.sky_condition, self.visibility, self.wind_speed,
                self.pressure, self.humidity, self.altimeter, self.rain, self.thunderstorm,
                self.snow, self.fog, self.mist, self.freezing]

    # NAIVE BAYES
    def get_categorical_properties(self):
        return [str(self.rain), str(self.thunderstorm), str(self.snow),
                str(self.fog), str(self.mist), str(self.freezing) , str(self.sky_condition)]

    def get_numerical_properties(self):
        return [self.temp, self.visibility, self.wind_speed, self.pressure,
                self.humidity, self.altimeter]

    # CORPUS
    def get_corpus_properties(self):
        return [self.temp, self.sky_condition, self.wind_speed,
                self.pressure, self.humidity, self.altimeter, self.rain,
                self.snow, self.fog, self.mist, self.freezing]

    def get_time_hour(self, time):
        if len(str(time)) <= 2:
            return str(time)
        time = str(time).zfill(4)
        time = datetime.strptime(time, '%M%S') - timedelta(hours=5)
        time = datetime.strftime(time,'%M%S')
        if len(time) == 3:
            return time[0]
        else:
            return time[0] + time[1]

    def set_codesum(self, codesum):
        code = self.process_code_sum(codesum)
        self.code_sum = code
        self.rain = self.process_rain_code(code)
        self.thunderstorm = self.process_thunderstorm_code(code)
        self.snow = self.process_snow_code(code)
        self.fog = self.process_fog_code(code)
        self.mist = self.process_mist_code(code)
        self.freezing = self.process_freezing_code(code)

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

    #Properties

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if len(str(date).split('-')) < 1:
            date = str(date)
            year, month, day = date[0:4], date[4:6], date[6:8]
            date = year + '-' + month + '-' + day
        self._date = date

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, temp):
        temp = str(temp)
        if temp == 'M' or temp.strip() == '':
            self._temp = None
        else:
            self._temp = float(temp)

    @property
    def sky_condition(self):
        return self._sky_condition

    @sky_condition.setter
    def sky_condition(self, sky_condition):
        sky_condition = str(sky_condition)
        if sky_condition == 'M' or sky_condition.strip() == '':
            self._sky_condition = None
        else:
            self._sky_condition = str(sky_condition)

    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, visibility):
        visibility = str(visibility)
        if visibility == 'M' or visibility.strip() == '':
            self._visibility = None
        else:
            self._visibility = float(visibility)

    @property
    def wind_speed(self):
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, wind_speed):
        wind_speed = str(wind_speed)
        if wind_speed == 'M' or wind_speed.strip() == '':
            self._wind_speed = None
        else:
            self._wind_speed = float(wind_speed)

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, pressure):
        pressure = str(pressure)
        if pressure == 'M' or pressure.strip() == '':
            self._pressure = None
        else:
            self._pressure = float(pressure)

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, humidity):
        humidity = str(humidity)
        if humidity == 'M' or humidity.strip() == '':
            self._humidity = None
        else:
            self._humidity = float(humidity)

    @property
    def altimeter(self):
        return self._altimeter

    @altimeter.setter
    def altimeter(self, altimeter):
        altimeter = str(altimeter)
        if altimeter == 'M' or altimeter.strip() == '':
            self._altimeter = None
        else:
            self._altimeter = float(altimeter)