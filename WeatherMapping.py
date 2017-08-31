import csv
import pandas as pd
from Models.Airport import Airport, Station
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
    def map_weather_fatures(self):
        training_stations = WeatherMapping.map_stations(original_stations_filename_2015, output_stations_filename_2015)
        testing_stations = WeatherMapping.map_stations(original_stations_filename_2016, output_stations_filename_2016)
        training_airports = WeatherMapping.map_airports(training_filename, output_training_airports_filename)
        testing_airports = WeatherMapping.map_airports(testing_filename, output_testing_airports_filename)
        WeatherMapping.map_airports_wban(training_airports, training_stations, output_training_airports_filename)
        WeatherMapping.map_airports_wban(testing_airports, testing_stations, output_testing_airports_filename)

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

WeatherMapping().map_weather_fatures()