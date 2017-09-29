import matplotlib.pyplot as plt
import csv
import numpy as np
import Constants
from Utils import Utils, WeatherType, FeatureEngineering

original_training_dataset_filename = 'Datasets/NewYork/Training/merged_training.csv'
original_testing_dataset_filename = 'Datasets/NewYork/Testing/merged_testing.csv'

training_dataset_filename = 'Datasets/TrainingDataset.csv'
testing_dataset_filename = 'Datasets/TestingDataset.csv'

training_hourly_weather_filename = 'Datasets/TrainingWeatherHourlyDataset.csv'
testing_hourly_weather_filename = 'Datasets/TestingWeatherHourlyDataset.csv'

training_corpus_filename = 'Datasets/TrainingCorpus.csv'
testing_corpus_filename = 'Datasets/TestingCorpus.csv'

class DatasetProcessing:
    def process_training_dataset(self):
        dataset = DatasetProcessing.cleanup(original_training_dataset_filename)
        dataset = DatasetProcessing.select_busiest_origin_airports(dataset, qty=45)
        dataset = DatasetProcessing.outliers_detection(dataset, adjust_outliers=True)
        #dataset = DatasetProcessing.holidays_feature_engineering(dataset)
        dataset = DatasetProcessing.days_to_holiday_feature_engineering(dataset)
        DatasetProcessing.create_processed_dataset(dataset, training_dataset_filename)

    def process_testing_dataset(self):
        dataset = DatasetProcessing.cleanup(original_testing_dataset_filename)
        #dataset = DatasetProcessing.holidays_feature_engineering(dataset)
        dataset = DatasetProcessing.days_to_holiday_feature_engineering(dataset)
        DatasetProcessing.create_processed_dataset(dataset, testing_dataset_filename)

    def cleanup(filename):
        dataset = Utils.load_csv(filename, include_cancelled=True)
        return dataset

    def select_busiest_origin_airports(dataset, qty=70):
        new_dataset = []
        x = {}
        for i in range(len(dataset)):
            origin_airport_name = dataset[i].origin_airport.name
            if origin_airport_name not in x:
                x[origin_airport_name] = 0
            x[origin_airport_name] += 1
        busiest_origin_airports = sorted(x, key=x.__getitem__, reverse=True)
        print(busiest_origin_airports)
        busiest_origin_airports = busiest_origin_airports[:qty]
        for i in range(len(dataset)):
            origin_airport_name = dataset[i].origin_airport.name
            busiest_origin_airports = set(busiest_origin_airports)
            if origin_airport_name in busiest_origin_airports:
                new_dataset.append(dataset[i])
        return new_dataset

    def outliers_detection(dataset, adjust_outliers = False):
        elapsed_time_values = []
        for i in range(len(dataset)):
            elapsed_time_values.append(float(dataset[i].elapsed_time))
        elapsed_time_mean = Utils.mean(elapsed_time_values)
        elapsed_time_stdev = Utils.stdev(elapsed_time_values)
        if adjust_outliers:
            new_dataset = []
            for i in range(len(dataset)):
                if float(dataset[i].elapsed_time) < 400.00:
                    new_dataset.append(dataset[i])
            return new_dataset
        elapsed_time_values = np.array(sorted(elapsed_time_values))
        print(elapsed_time_values)
        plt.figure()
        plt.boxplot([elapsed_time_values])
        plt.xticks([1], ['Tiempo estimado de vuelo'])
        plt.show()
        return dataset

    def holidays_feature_engineering(dataset):
        new_dataset = []
        for i in range(len(dataset)):
            flight = dataset[i]
            flight.set_holiday(type=1)
            new_dataset.append(flight)
        return new_dataset

    def days_to_holiday_feature_engineering(dataset):
        new_dataset = []
        for i in range(len(dataset)):
            flight = dataset[i]
            flight.set_days_to_holiday()
            new_dataset.append(flight)
        return new_dataset

    def create_processed_dataset(dataset, filename):
        dataset_list = []
        for i in range(len(dataset)):
            dataset_list.append(dataset[i].get_properties_array())
        wr = csv.writer(open(filename, "w+"))
        wr.writerows(dataset_list)

    def merge_training_files(self):
        Utils.merge_csv_files(Constants.monthly_training_folder,
                              Constants.month_labels,
                              Constants.output_training_merge_filename)

    def corpus_creation(self):
        DatasetProcessing.create_training_corpus()
        DatasetProcessing.create_testing_corpus()

    def create_training_corpus():
        header_array = ['MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'ORIGIN_AIRPORT', 'DEST_AIRPORT',
                        'DEPARTURE_TIME', 'FL_NUMBER', 'TAIL_NUMBER', 'ELAPSED_TIME', 'DAYS_TO_HOLIDAY',
                        'TEMPERATURE', 'SKY_CONTIDION', 'WIND_SPEED', 'PRESSURE', 'HUMIDITY',
                        'ALTIMETER', 'RAIN', 'SNOW', 'FOG', 'MIST', 'FREEZING', 'DELAYED']
        training_dataset = Utils.load_processed_dataset(training_hourly_weather_filename, include_weather=True,
                                                        weather_type=WeatherType.HOURLY)
        training_array = []
        print(len(training_dataset))
        for i in range(len(training_dataset)):
            training_array.append(training_dataset[i].get_corpus_properties())
        print(len(training_array))
        print(training_array[0])
        wr = csv.writer(open(training_corpus_filename, "w+"))
        wr.writerow(header_array)
        wr.writerows(training_array)

    def create_testing_corpus():
        header_array = ['MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'ORIGIN_AIRPORT', 'DEST_AIRPORT',
                        'DEPARTURE_TIME', 'FL_NUMBER', 'TAIL_NUMBER', 'ELAPSED_TIME', 'DAYS_TO_HOLIDAY',
                        'TEMPERATURE', 'SKY_CONTIDION', 'WIND_SPEED', 'PRESSURE', 'HUMIDITY',
                        'ALTIMETER', 'RAIN', 'SNOW', 'FOG', 'MIST', 'FREEZING', 'DELAYED']
        testing_dataset = Utils.load_processed_dataset(testing_hourly_weather_filename, include_weather=True,
                                                        weather_type=WeatherType.HOURLY)
        testing_array = []
        print(len(testing_dataset))
        for i in range(len(testing_dataset)):
            testing_array.append(testing_dataset[i].get_corpus_properties())
        print(len(testing_array))
        print(testing_array[0])
        wr = csv.writer(open(testing_corpus_filename, "w+"))
        wr.writerow(header_array)
        wr.writerows(testing_array)

DatasetProcessing().corpus_creation()