import csv
import math
import datetime
import pandas as pd
import numpy as np
from Models.Flight import Flight, Constants
from Models.Weather import Weather
from Models.HourlyWeather import HourlyWeather
from enum import Enum

class FeatureEngineering(Enum):
    HOLIDAY = 0
    DAYSTOHOLIDAY = 1

class WeatherType(Enum):
    DAILY = 0
    HOURLY = 1

class Utils:
    def load_csv(filename, include_cancelled=False):
        lines = csv.reader(open(filename, "r"))
        next(lines)
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            estimated_departure_time = dataset[i][14]
            real_departure_time = dataset[i][15]
            floating_point_pos = real_departure_time.find('.')
            if floating_point_pos != -1:
                real_departure_time = real_departure_time[0:floating_point_pos]
                dataset[i][15] = real_departure_time
            elapsed_time = dataset[i][22]
            tail_number = dataset[i][8]
            if include_cancelled:
                dataset_has_time_data = (len(estimated_departure_time) >= 1) and \
                                             (real_departure_time == '' or len(real_departure_time) >= 1)
            else:
                dataset_has_time_data = len(estimated_departure_time) >= 1 and \
                                             len(real_departure_time) >= 1
            dataset_has_missing_data = elapsed_time == '' or tail_number == ''
            if dataset_has_time_data and not dataset_has_missing_data:
                proccessed_dataset.append(Flight(dataset[i][1], dataset[i][2],
                                                 dataset[i][3], dataset[i][4],
                                                 dataset[i][5], dataset[i][6],
                                                 dataset[i][7], dataset[i][8],
                                                 dataset[i][9], dataset[i][10],
                                                 dataset[i][11], dataset[i][12],
                                                 dataset[i][13], dataset[i][14],
                                                 dataset[i][15], dataset[i][22],
                                                 dataset[i][23]))
        return proccessed_dataset

    def load_processed_dataset(filename, feature=FeatureEngineering.DAYSTOHOLIDAY,
                               include_weather=False, weather_type=WeatherType.DAILY):
        lines = csv.reader(open(filename, "r"))
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            flight = Flight(dataset[i][0], dataset[i][1],
                                dataset[i][2], dataset[i][3],
                                dataset[i][4], dataset[i][5],
                                dataset[i][6], dataset[i][7],
                                dataset[i][8], dataset[i][9],
                                dataset[i][10], dataset[i][11],
                                dataset[i][12], dataset[i][13],
                                dataset[i][14], dataset[i][15],
                                dataset[i][16])
            if dataset[i][17] is not None:
                if feature == FeatureEngineering.HOLIDAY:
                    flight.holiday = dataset[i][17]
                else:
                    flight.days_to_holiday = dataset[i][17]
            if dataset[i][18] is not None:
                flight.origin_airport.wban = Utils.remove_floating_point(dataset[i][18])
            if include_weather:
                if len(dataset[i]) < 27:
                    weather = None
                else:
                    if weather_type == WeatherType.DAILY:
                        weather = Weather(dataset[i][18], flight.date, dataset[i][21],
                                          dataset[i][19], dataset[i][20], dataset[i][22],
                                          dataset[i][23], dataset[i][24], dataset[i][25])
                    else:
                        weather = HourlyWeather(dataset[i][18], flight.date, flight.get_departure_time_hour(),
                                                dataset[i][19], dataset[i][20], dataset[i][21],
                                                dataset[i][22], dataset[i][23], dataset[i][24],
                                                dataset[i][25])
                    weather.rain = float(dataset[i][26])
                    weather.thunderstorm = float(dataset[i][27])
                    weather.snow = float(dataset[i][28])
                    weather.fog = float(dataset[i][29])
                    weather.mist = float(dataset[i][30])
                    weather.freezing = float(dataset[i][31])
                if weather_type == WeatherType.DAILY:
                    flight.weather = weather
                else:
                    flight.hourly_weather = weather
            proccessed_dataset.append(flight)
        return proccessed_dataset

    # Weather datasets

    def load_daily_weather_dataset(filename):
        weather_array = []
        df = pd.read_csv(filename)
        header = list(df.columns.values)
        df = df.fillna('')
        df = df.as_matrix()
        for i in range(len(df)):
            w = df[i]
            wban = str(w[header.index("WBAN")]).zfill(5)
            weather = Weather(wban, w[header.index("DATE")], w[header.index("TMAX")],
                                  w[header.index("TMIN")], w[header.index("TAVG")],
                                  w[header.index("SNOWFALL")], w[header.index("WATER")],
                                  w[header.index("PRESSURE")], w[header.index("SPEED")],
                                  w[header.index("CODESUM")])
            weather_array.append(weather)
        return weather_array

    def load_hourly_weather_dataset(filename, include_codesum=False):
        weather_array = []
        df = pd.read_csv(filename)
        header = list(df.columns.values)
        df = df.fillna('')
        df = df.as_matrix()
        for i in range(len(df)):
            w = df[i]
            wban = str(w[header.index("WBAN")]).zfill(5)
            weather = HourlyWeather(wban, w[header.index("DATE")], w[header.index("TIME")],
                                w[header.index("TEMP")], w[header.index("SKY")],
                                w[header.index("VISIBILITY")], w[header.index("SPEED")],
                                w[header.index("PRESSURE")], w[header.index("HUMIDITY")],
                                w[header.index("ALTIMETER")])
            if include_codesum:
                weather.set_codesum(w[header.index("CODESUM")])
            weather_array.append(weather)
        return weather_array

    # Files Handler

    def merge_csv_files(file_prefix, month_labels, output_filename, file_ext=".csv"):
        results = pd.read_csv(file_prefix + month_labels[0] + file_ext).dropna(how='all')
        for i in range(1, len(month_labels)):
            namedf = pd.read_csv(file_prefix + month_labels[i] + file_ext).dropna(how='all')
            results = results.append(namedf)
        results.to_csv(output_filename, encoding='utf-8')

    # Date Helpers

    def get_prior_day_date(day, month, year):
        string_date = Utils.get_date_string(day, month, year)
        date = datetime.datetime.strptime(string_date, "%d/%m/%Y").date()
        date = date + datetime.timedelta(days=-1)
        return date.strftime('%d/%m/%Y')

    def get_posterior_day_date(day, month, year):
        string_date = Utils.get_date_string(day, month, year)
        date = datetime.datetime.strptime(string_date, "%d/%m/%Y").date()
        date = date + datetime.timedelta(days=1)
        return date.strftime('%d/%m/%Y')

    def get_date(day, month, year):
        string_date = Utils.get_date_string(day, month, year)
        date = datetime.datetime.strptime(string_date, "%d/%m/%Y").date()
        return date.strftime('%d/%m/%Y')

    def get_date_string(day, month, year):
        return day + '/' + month + '/' + year

    def get_near_dates(day, month, year, include_current=False):
        if day == '1' and month == '1':
            post_date = Utils.get_posterior_day_date(day, month, year)
            prior_date = post_date
        elif day == '31' and month == '12':
            prior_date = Utils.get_prior_day_date(day, month, year)
            post_date = prior_date
        else:
            prior_date = Utils.get_prior_day_date(day, month, year)
            post_date = Utils.get_posterior_day_date(day, month, year)
        if include_current:
            current = Utils.get_date(day, month, year)
            return prior_date, current, post_date
        return  prior_date, post_date

    def days_difference_between_dates(first_date, second_date):
        f_date = datetime.datetime.strptime(first_date, "%d/%m/%Y").date()
        s_date = datetime.datetime.strptime(second_date, "%d/%m/%Y").date()
        delta = s_date - f_date
        return delta.days

    # Math

    def mean(values):
        values = [x for x in values if x is not None]
        return sum(values) / float(len(values))

    def stdev(values):
        values = [x for x in values if x is not None]
        avg = Utils.mean(values)
        variance = sum([pow(x - avg, 2) for x in values]) / float(len(values) - 1)
        return math.sqrt(variance)

    # String

    def remove_floating_point(value):
        floating_point_pos = value.find('.')
        if floating_point_pos != -1:
            return value[0:floating_point_pos]
        else:
            return ValueError

    # Pandas

    def load_df_from_json(json):
        df_header = Constants.df_header
        print(df_header)
        print(json)
        month, day_of_month, day_of_week, days_to_holiday = Utils.get_date_characteristics(json['date'])
        origin, dest, dep, fl_num, tail_num, elapsed = Utils.get_base_characteristics(json)
        temp, sky, wind, press, hum, alt = Utils.get_weather_characteristics(json)
        rain, snow, fog, mist, freezing, delayed = Utils.get_binary_characteristics(json)
        array = [month, day_of_month, day_of_week, origin, dest, dep,
                 fl_num, tail_num, elapsed, days_to_holiday, temp, sky,
                 wind, press, hum, alt, rain, snow, fog, mist, freezing, delayed]
        df = pd.DataFrame(np.array(array).reshape(1, 22), columns=df_header)
        df = df.replace('', np.nan)
        df[["DELAYED"]] = df[["DELAYED"]].astype(int).astype(bool)
        print(df)
        return df


    def get_date_characteristics(string_date):
        if string_date == '':
            return None, None, None, 20
        date = datetime.datetime.strptime(string_date, "%d/%m/%Y").date()
        month = str(date.month)
        day_of_month = str(date.day)
        day_of_week = str(date.weekday() + 1)
        return month, day_of_month, day_of_week, 10

    def get_base_characteristics(json):
        origin = json['origin']
        dest = json['destination']
        dep = Utils.get_dep(json['departure'])
        fl_num = json['flightNumber']
        tail_num = json['tailNumber']
        elapsed = json['estimatedTime']
        return origin, dest, dep, fl_num, tail_num, elapsed

    def get_weather_characteristics(json):
        temp = json['temp']
        sky = json['skyCondition']
        wind = json['windSpeed']
        press = json['pressure']
        hum = json['humidity']
        alt = json['altimeter']
        return temp, sky, wind, press, hum, alt

    def get_binary_characteristics(json):
        rain = json['rain']
        snow = json['snow']
        fog = json['fog']
        mist = json['mist']
        freezing = json['freezing']
        delayed = 0
        return rain, snow, fog, mist, freezing, delayed

    def get_dep(dep_time):
        if dep_time == '':
            return None
        arr = dep_time.split(':')
        time = str(int(arr[0]))
        return time