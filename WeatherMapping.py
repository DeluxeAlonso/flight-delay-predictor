import csv
import pandas as pd
import Constants
from Models.Airport import Airport, Station
from Models.Weather import Weather
from Utils import Utils

original_stations_filename_2015 = 'WeatherMappingFiles/Stations/2015stations.txt'
original_stations_filename_2016 = 'WeatherMappingFiles/Stations/2016stations.txt'
output_stations_filename_2015 = 'WeatherMappingFiles/Stations/2015_stations.csv'
output_stations_filename_2016 = 'WeatherMappingFiles/Stations/2016_stations.csv'

training_filename = 'Datasets/TrainingDataset.csv'
output_training_airports_filename = 'WeatherMappingFiles/training_airports.csv'
testing_filename = 'Datasets/TestingDataset.csv'
output_testing_airports_filename = 'WeatherMappingFiles/testing_airports.csv'

class WeatherMapping:
    def map_weather_features(self):
        training_stations, testing_stations, training_airports, testing_airports = WeatherMapping.map_variables()
        Utils.merge_csv_files(Constants.weather_daily_training_folder, Constants.weather_daily_training_labels,
                              Constants.output_training_weather_merged_filename, file_ext=".txt")
        Utils.merge_csv_files(Constants.weather_daily_testing_folder, Constants.weather_daily_testing_labels,
                              Constants.output_testing_weather_merged_filename, file_ext=".txt")
        training_weather = WeatherMapping.create_weather_file(training_airports, Constants.output_training_weather_merged_filename,
                                           Constants.output_training_weather_filename)
        testing_weather = WeatherMapping.create_weather_file(testing_airports, Constants.output_testing_weather_merged_filename,
                                           Constants.output_testing_weather_filename)

    def map_variables():
        training_stations = WeatherMapping.map_stations(original_stations_filename_2015, output_stations_filename_2015)
        testing_stations = WeatherMapping.map_stations(original_stations_filename_2016, output_stations_filename_2016)
        training_airports = WeatherMapping.map_airports(training_filename, output_training_airports_filename)
        testing_airports = WeatherMapping.map_airports(testing_filename, output_testing_airports_filename)
        WeatherMapping.map_airports_wban(training_airports, training_stations, output_training_airports_filename)
        WeatherMapping.map_airports_wban(testing_airports, testing_stations, output_testing_airports_filename)
        return training_stations, testing_stations, training_airports, testing_airports

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
        print(station_names)
        for i in range(len(airports)):
            try:
                index = station_names.index(airports[i].name)
            except ValueError:
                index = -1
            if index != -1:
                airports[i].wban = stations[index].wban
        WeatherMapping.create_airports_file(airports, output_filename)
        return airports

    def create_weather_file(airports, filename, output_filename):
        weather_list = []
        airport_wbans = list(map(lambda x: x.wban, airports))
        df = pd.read_csv(filename)
        header = list(df.columns.values)
        df = df.as_matrix()
        for i in range(len(df)):
            w = df[i]
            wban = w[header.index("WBAN")]
            if str(wban) in airport_wbans:
                weather = Weather(wban, w[header.index("YearMonthDay")], w[header.index("Tmax")],
                                  w[header.index("Tmin")], w[header.index("Tavg")],
                                  w[header.index("SnowFall")], w[header.index("PrecipTotal")],
                                  w[header.index("StnPressure")], w[header.index("AvgSpeed")])
                weather_list.append(weather.get_properties_array())
        wr = csv.writer(open(output_filename, "w+"))
        wr.writerow(['WBAN', 'DATE', 'TMIN', 'TAVG', 'TMAX', 'SNOWFALL', 'WATER', 'PRESSURE', 'SPEED'])
        wr.writerows(weather_list)
        return weather_list


WeatherMapping().map_weather_features()