import csv
from Models.Station import Station

original_stations_filename = 'WeatherMappingFiles/Stations/stations.txt'
output_stations_filename = 'WeatherMappingFiles/Stations/stations.csv'

class WeatherMapping:
    def map_stations(self):
        with open(original_stations_filename, "r") as f:
            code, name, latitude, longitude, timezone = WeatherMapping.get_station_header_indexes(f.readline())
            stations = []
            for line in f:
                array = line.split('|')
                station = Station(array[code], array[name], array[latitude],
                                  array[longitude], array[timezone].strip('\n'))
                stations.append(station)
            print(stations[0].get_properties_array())
        WeatherMapping.create_stations_file(stations, output_stations_filename)

    def get_station_header_indexes(line):
        line_array = line.split('|')
        print(line_array)
        code = line_array.index('WBAN')
        name = line_array.index('CallSign')
        latitude = line_array.index('Latitude')
        longitude = line_array.index('Longitude')
        timezone = line_array.index('TimeZone\n')
        return code, name, latitude, longitude, timezone

    def create_stations_file(stations, filename):
        stations_list = []
        for i in range(len(stations)):
            stations_list.append(stations[i].get_properties_array())
        wr = csv.writer(open(filename, "w+"))
        wr.writerow(['ID', 'NAME', 'LATITUDE', 'LONGITUDE', 'TIMEZONE'])
        wr.writerows(stations_list)

WeatherMapping().map_stations()