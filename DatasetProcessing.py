import matplotlib.pyplot as plt
import csv
from Utils import Utils
import numpy as np

original_training_dataset_filename = 'Datasets/NewYork/training.csv'
training_dataset_filename = 'Datasets/TrainingDataset.csv'

class DatasetProcessing:
    def process_datasets(self):
        dataset = DatasetProcessing.cleanup()
        dataset = DatasetProcessing.select_busiest_origin_airports(dataset, qty=45)
        DatasetProcessing.outliers_detection(dataset, adjust_outliers=True)
        DatasetProcessing.create_processed_dataset(dataset, training_dataset_filename)

    def cleanup():
        dataset = Utils.load_csv(original_training_dataset_filename, include_cancelled=True)
        return dataset

    def select_busiest_origin_airports(dataset, qty=70):
        new_dataset = []
        x = {}
        for i in range(len(dataset)):
            origin_airport_name = dataset[i].origin_airport_name
            if origin_airport_name not in x:
                x[origin_airport_name] = 0
            x[origin_airport_name] += 1
        busiest_origin_airports = sorted(x, key=x.__getitem__, reverse=True)
        print(busiest_origin_airports)
        busiest_origin_airports = busiest_origin_airports[:qty]
        for i in range(len(dataset)):
            origin_airport = dataset[i].origin_airport_name
            busiest_origin_airports = set(busiest_origin_airports)
            if origin_airport in busiest_origin_airports:
                new_dataset.append(dataset[i])
        return new_dataset

    def outliers_detection(dataset, adjust_outliers = False):
        elapsed_time_values = []
        for i in range(len(dataset)):
            elapsed_time_values.append(float(dataset[i].elapsed_time))
        elapsed_time_mean = Utils.mean(elapsed_time_values)
        elapsed_time_stdev = Utils.stdev(elapsed_time_values)
        print(elapsed_time_mean)
        print(elapsed_time_stdev)
        if adjust_outliers:
            elapsed_time_values = []
            for i in range(len(dataset)):
                if float(dataset[i].elapsed_time) >= 500.00:
                    dataset[i].set_elapsed_time(int(elapsed_time_mean))
                elapsed_time_values.append(float(dataset[i].elapsed_time))
        elapsed_time_values = np.array(sorted(elapsed_time_values))
        print(elapsed_time_values)
        plt.figure()
        plt.boxplot([elapsed_time_values])
        plt.xticks([1], ['Tiempo estimado de vuelo'])
        plt.show()

    def create_processed_dataset(dataset, filename):
        dataset_list = []
        for i in range(len(dataset)):
            dataset_list.append(dataset[i].get_all_property_array())
        wr = csv.writer(open(filename, "w+"))
        wr.writerows(dataset_list)

DatasetProcessing().process_datasets()