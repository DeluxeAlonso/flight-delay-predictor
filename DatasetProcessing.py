import matplotlib.pyplot as plt
import csv
import numpy as np
import Constants
from Utils import Utils

original_training_dataset_filename = 'Datasets/NewYork/Training/merged_training.csv'
training_dataset_filename = 'Datasets/TrainingDataset.csv'

original_testing_dataset_filename = 'Datasets/NewYork/Testing/merged_testing.csv'
testing_dataset_filename = 'Datasets/TestingDataset.csv'

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

DatasetProcessing().process_testing_dataset()