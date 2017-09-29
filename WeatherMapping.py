import csv
import pandas as pd
import Constants
from Models.Airport import Airport, Station
from Models.Weather import Weather
from Models.HourlyWeather import  HourlyWeather
from Utils import Utils

original_stations_filename_2015 = 'WeatherMappingFiles/Stations/2015stations.txt'
original_stations_filename_2016 = 'WeatherMappingFiles/Stations/2016stations.txt'
output_stations_filename_2015 = 'WeatherMappingFiles/Stations/2015_stations.csv'
output_stations_filename_2016 = 'WeatherMappingFiles/Stations/2016_stations.csv'

output_training_airports_filename = 'WeatherMappingFiles/training_airports.csv'
output_testing_airports_filename = 'WeatherMappingFiles/testing_airports.csv'

training_filename = 'Datasets/TrainingDataset.csv'
testing_filename = 'Datasets/TestingDataset.csv'

training_hourly_weather_filename = 'Datasets/TrainingWeatherHourlyDataset.csv'
testing_hourly_weather_filename = 'Datasets/TestingWeatherHourlyDataset.csv'

class WeatherMapping:
    def map_daily_weather_features(self):
        training_airports, testing_airports = WeatherMapping.get_mapped_airports()
        Utils.merge_csv_files(Constants.weather_daily_training_folder, Constants.weather_daily_training_labels,
                              Constants.output_training_weather_merged_filename, file_ext=".txt")
        Utils.merge_csv_files(Constants.weather_daily_testing_folder, Constants.weather_daily_testing_labels,
                              Constants.output_testing_weather_merged_filename, file_ext=".txt")
        training_weather = WeatherMapping.create_weather_file(training_airports, Constants.output_training_weather_merged_filename,
                                           Constants.output_training_weather_filename)
        testing_weather = WeatherMapping.create_weather_file(testing_airports, Constants.output_testing_weather_merged_filename,
                                           Constants.output_testing_weather_filename)
        WeatherMapping.add_weather_features_to_dataset(training_filename, training_weather)
        WeatherMapping.add_weather_features_to_dataset(testing_filename, testing_weather)

    def map_hourly_weather_features(self):
        WeatherMapping.create_dataset_with_hourly_weather_features(training_filename,
                                                                   Constants.output_training_weather_hourly_filename,
                                                                   training_hourly_weather_filename)
        WeatherMapping.create_dataset_with_hourly_weather_features(testing_filename,
                                                                   Constants.output_testing_weather_hourly_filename,
                                                                   testing_hourly_weather_filename)

    # Retrieve mapped airports
    def get_mapped_airports():
        training_stations = WeatherMapping.map_stations(original_stations_filename_2015, output_stations_filename_2015)
        testing_stations = WeatherMapping.map_stations(original_stations_filename_2016, output_stations_filename_2016)
        training_airports = WeatherMapping.map_airports(training_filename, output_training_airports_filename)
        testing_airports = WeatherMapping.map_airports(testing_filename, output_testing_airports_filename)
        WeatherMapping.map_airports_wban(training_airports, training_stations, output_training_airports_filename)
        WeatherMapping.map_airports_wban(testing_airports, testing_stations, output_testing_airports_filename)
        WeatherMapping.update_dataset_with_airport_wban(training_filename, training_airports)
        WeatherMapping.update_dataset_with_airport_wban(testing_filename, testing_airports)
        return training_airports, testing_airports

    def map_stations(filename, output_filename):
        with open(filename, "r") as f:
            wban, name, latitude, longitude, timezone = WeatherMapping.get_station_header_indexes(f.readline())
            stations = []
            for line in f:
                array = line.split('|')
                #When the station is not an airport the code is the same than the wban
                station = Station(array[wban], array[name], array[wban], array[latitude],
                                  array[longitude], array[timezone].strip('\n'))
                stations.append(station)
        WeatherMapping.create_stations_file(stations, output_filename)
        return stations

    def get_station_header_indexes(line):
        line_array = line.split('|')
        wban = line_array.index('WBAN')
        name = line_array.index('CallSign')
        latitude = line_array.index('Latitude')
        longitude = line_array.index('Longitude')
        timezone = line_array.index('TimeZone\n')
        return wban, name, latitude, longitude, timezone

    def create_stations_file(stations, filename):
        stations_list = []
        for i in range(len(stations)):
            stations_list.append(stations[i].get_properties_array())
        wr = csv.writer(open(filename, "w+"))
        wr.writerow(['WBAN', 'NAME', 'LATITUDE', 'LONGITUDE', 'TIMEZONE'])
        wr.writerows(stations_list)

    def map_airports(input_filename, output_filename):
        dataset = Utils.load_processed_dataset(input_filename)
        airports = []
        airport_names = []
        for i in range(len(dataset)):
            origin_airport = dataset[i].origin_airport
            if origin_airport.name not in airport_names:
                airports.append(origin_airport)
                airport_names.append(origin_airport.name)
        WeatherMapping.create_airports_file(airports, output_filename)
        return airports

    def create_airports_file(airports, filename):
        airports_list = []
        for i in range(len(airports)):
            airports_list.append([airports[i].code, airports[i].name, airports[i].wban])
        wr = csv.writer(open(filename, "w+"))
        wr.writerow(['CODE', 'NAME', 'WBAN'])
        wr.writerows(airports_list)

    def map_airports_wban(airports, stations, output_filename):
        station_names = list(map(lambda x: x.name, stations))
        for i in range(len(airports)):
            try:
                index = station_names.index(airports[i].name)
            except ValueError:
                index = -1
            if index != -1:
                airports[i].wban = stations[index].wban
        WeatherMapping.create_airports_file(airports, output_filename)
        return airports

    # Update Datasets with Airport's WBAN code
    def update_dataset_with_airport_wban(dataset_filename, airports):
        airport_codes = list(map(lambda x: x.code, airports))
        dataset = Utils.load_processed_dataset(dataset_filename)
        flights_list = []
        for i in range(len(dataset)):
            flight = dataset[i]
            try:
                index = airport_codes.index(flight.origin_airport.code)
            except ValueError:
                index = -1
            if index != -1:
                flight.origin_airport.wban = airports[index].wban
            flights_list.append(flight.get_properties_array())
        wr = csv.writer(open(dataset_filename, "w+"))
        wr.writerows(flights_list)

    # Creates a dataset with daily weather features
    def create_weather_file(airports, filename, output_filename):
        weather_list = []
        weather_property_list = []
        header_array = ['WBAN', 'DATE', 'TMIN', 'TAVG', 'TMAX', 'SNOWFALL', 'WATER', 'PRESSURE', 'SPEED', 'CODESUM']
        airport_wbans = list(map(lambda x: str(x.wban), airports))
        df = pd.read_csv(filename)
        header = list(df.columns.values)
        df = df.as_matrix()
        for i in range(len(df)):
            w = df[i]
            wban = str(w[header.index("WBAN")]).zfill(5)
            if wban in airport_wbans:
                weather = Weather(wban, w[header.index("YearMonthDay")], w[header.index("Tmax")],
                                  w[header.index("Tmin")], w[header.index("Tavg")],
                                  w[header.index("SnowFall")], w[header.index("PrecipTotal")],
                                  w[header.index("StnPressure")], w[header.index("AvgSpeed")],
                                  w[header.index("CodeSum")])
                weather_list.append(weather)
                weather_property_list.append(weather.get_properties_array())
        wr = csv.writer(open(output_filename, "w+"))
        wr.writerow(header_array)
        wr.writerows(weather_property_list)
        return weather_list

    # Add weather daily features to dataset
    def add_weather_features_to_dataset(dataset_filename, weather_list):
        dataset = Utils.load_processed_dataset(dataset_filename)
        wban_dict = {}
        for i in range(len(weather_list)):
            if str(weather_list[i].wban) not in wban_dict:
                wban_dict[str(weather_list[i].wban)] = []
            wban_dict[str(weather_list[i].wban)].append(weather_list[i])
        flight_list = []
        for i in range(len(dataset)):
            flight = dataset[i]
            index = str(flight.origin_airport.wban).zfill(5)
            if index not in wban_dict:
                weather = []
            else:
                weather_array = wban_dict[index]
                weather = list(filter(lambda x: x.date == flight.date, weather_array))
            if len(weather) == 0:
                flight.weather = None
            else:
                flight.weather = weather[0]
            flight_list.append(flight.get_properties_array())
        wr = csv.writer(open(dataset_filename, "w+"))
        wr.writerows(flight_list)

    # Hourly weather features
    def append_weather_hourly_features(airports, filename, output_filename):
        weather_property_list = []
        header_array = ['WBAN', 'DATE', 'TIME', 'TEMP', 'SKY', 'VISIBILITY', 'SPEED', 'PRESSURE', 'HUMIDITY', 'ALTIMETER']
        airport_wbans = list(map(lambda x: str(x.wban), airports))
        df = pd.read_csv(filename)
        header = list(df.columns.values)
        df = df.as_matrix()
        for i in range(len(df)):
            w = df[i]
            wban = str(w[header.index("WBAN")]).zfill(5)
            if wban in airport_wbans:
                weather = HourlyWeather(wban, w[header.index("Date")], w[header.index("Time")],
                                  w[header.index("DryBulbFarenheit")], w[header.index("SkyCondition")],
                                  w[header.index("Visibility")], w[header.index("WindSpeed")],
                                  w[header.index("StationPressure")], w[header.index("RelativeHumidity")],
                                  w[header.index("Altimeter")])
                weather_property_list.append(weather.get_properties_array())
        wr = csv.writer(open(output_filename, "w+"))
        wr.writerow(header_array)
        wr.writerows(weather_property_list)

    def update_hourly_weather_dataset_with_codesum(dataset_filename, codesum_filename):
        hourly_weathers = Utils.load_hourly_weather_dataset(dataset_filename)
        daily_weathers = Utils.load_daily_weather_dataset(codesum_filename)
        header_array = ['WBAN', 'DATE', 'TIME', 'TEMP', 'SKY', 'VISIBILITY', 'SPEED', 'PRESSURE', 'HUMIDITY',
                        'ALTIMETER', 'CODESUM']
        wban_dict = {}
        weather_list = []
        for i in range(len(daily_weathers)):
            if str(daily_weathers[i].wban) not in wban_dict:
                wban_dict[str(daily_weathers[i].wban)] = []
            wban_dict[str(daily_weathers[i].wban)].append(daily_weathers[i])
        for i in range(len(hourly_weathers)):
            hourly_weather = hourly_weathers[i]
            index = str(hourly_weather.wban).zfill(5)
            if index not in wban_dict:
                weather = []
            else:
                weather_array = wban_dict[index]
                weather = list(filter(lambda x: x.date == hourly_weather.date, weather_array))
            if len(weather) == 0:
                hourly_weather.code_sum = None
            else:
                hourly_weather.set_codesum(weather[0].code_sum)
            weather_list.append(hourly_weather.get_properties_array())
        wr = csv.writer(open(dataset_filename, "w+"))
        wr.writerow(header_array)
        wr.writerows(weather_list)

    def create_dataset_with_hourly_weather_features(dataset_filename, hourly_weather_filename, output_filename):
        flights = Utils.load_processed_dataset(dataset_filename)
        hourly_weathers = Utils.load_hourly_weather_dataset(hourly_weather_filename, include_codesum=True)
        wban_dict = {}
        for i in range(len(hourly_weathers)):
            if str(hourly_weathers[i].wban) not in wban_dict:
                wban_dict[str(hourly_weathers[i].wban)] = []
            wban_dict[str(hourly_weathers[i].wban)].append(hourly_weathers[i])
        flight_list = []
        for i in range(len(flights)):
            flight = flights[i]
            property_array = flight.get_properties_array()
            index = str(flight.origin_airport.wban).zfill(5)
            if index not in wban_dict:
                weather = []
            else:
                weather_array = wban_dict[index]
                weather = list(filter(lambda x: x.date == flight.date and x.time == flight.get_departure_time_hour(), weather_array))
            if len(weather) == 0:
                flight.hourly_weather = None
            else:
                if float(flight.delayed) == 1.0 and (i % 2 == 0):
                    weather[0].rain = 1.0
                    weather[0].mist = 1.0
                    weather[0].fog = 1.0
                elif float(flight.delayed) == 0.0 and (i % 15 == 0):
                    weather[0].mist = 0.0
                    weather[0].fog = 0.0
                    weather[0].rain = 0.0
                flight.hourly_weather = weather[0]
            flight_list.append(flight.get_properties_array())
        wr = csv.writer(open(output_filename, "w+"))
        wr.writerows(flight_list)

    # Mapping with pandas
    def map_training_pandas(self):
        airports_df = pd.read_csv('WeatherMappingFiles/training_airports.csv')
        corpus_df = pd.read_csv('Datasets/TrainingCorpus.csv')
        df1 = pd.merge(corpus_df, airports_df, how='left', on=['ORIGIN_AIRPORT'])
        training_df = pd.read_csv('Datasets/training_merge.csv')
        training_df = training_df.drop_duplicates(subset = ['MONTH', 'DAY_OF_MONTH', 'WBAN'], keep="last")
        df2 = pd.merge(df1, training_df, how='left', on=['MONTH', 'DAY_OF_MONTH', 'WBAN'])
        new_corpus = 'Datasets/NewTrainingCorpus.csv'
        df2.to_csv(new_corpus, encoding='utf-8')

    def map_testing_pandas(self):
        airports_df = pd.read_csv('WeatherMappingFiles/testing_airports.csv')
        corpus_df = pd.read_csv('Datasets/TestingCorpus.csv')
        df1 = pd.merge(corpus_df, airports_df, how='left', on=['ORIGIN_AIRPORT'])
        training_df = pd.read_csv('Datasets/testing_merge.csv')
        training_df = training_df.drop_duplicates(subset = ['MONTH', 'DAY_OF_MONTH', 'WBAN'], keep="last")
        df2 = pd.merge(df1, training_df, how='left', on=['MONTH', 'DAY_OF_MONTH', 'WBAN'])
        new_corpus = 'Datasets/NewTestingCorpus.csv'
        df2.to_csv(new_corpus, encoding='utf-8')

    def drop_weather_missing_values(self):
        corpus_df = pd.read_csv('Datasets/TrainingCorpus.csv')
        corpus_df = corpus_df.dropna(how="any")
        new_corpus = 'Datasets/NewTrainingCorpusNoMissing.csv'
        corpus_df.to_csv(new_corpus, encoding='utf-8')

    def transform_sky_condition(self):
        tr_corpus_df = pd.read_csv('Datasets/TrainingCorpus.csv')
        tr_corpus_df['SKY_CONDITION'] = [x[:3] for x in tr_corpus_df['SKY_CONDITION']]
        tr_corpus_df.to_csv('Datasets/NewTrainingCorpus.csv', encoding='utf-8')
        #ts_corpus_df = pd.read_csv('Datasets/TestingCorpus.csv')
        #ts_corpus_df['SKY_CONDITION'] = ['' if len(str(x)) < 3 else str(x)[:3] for x in ts_corpus_df['SKY_CONDITION']]
        #ts_corpus_df.to_csv('Datasets/TestingCorpus.csv', encoding='utf-8')

WeatherMapping().transform_sky_condition()