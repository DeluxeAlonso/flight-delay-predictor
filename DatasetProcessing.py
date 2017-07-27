import matplotlib.pyplot as plt
import csv
from Utils import Utils
import numpy as np

original_dataset_filename = 'Datasets/NewYork/training.csv'
naive_bayes_dataset_filename = 'Datasets/NaiveBayesDataset.csv'
random_forest_dataset_filename = 'Datasets/RandomForestDataset.csv'

class DatasetProcessing:
    def process_datasets(self):
        self.process_naive_bayes_dataset()
        self.processs_random_forest_dataset()

    def process_naive_bayes_dataset(self):
        dataset = DatasetProcessing.cleanup()
        dataset = DatasetProcessing.select_busiest_origin_airports(dataset, qty=500)
        DatasetProcessing.create_processed_dataset(dataset, naive_bayes_dataset_filename)
        print("Naive Bayes Dataset size {0}".format(len(dataset)))

    def processs_random_forest_dataset(self):
        dataset = DatasetProcessing.cleanup()
        dataset = DatasetProcessing.select_busiest_origin_airports(dataset, qty=500)
        DatasetProcessing.create_processed_dataset(dataset, random_forest_dataset_filename)
        print("Random Forest Dataset size {0}".format(len(dataset)))
        #DatasetProcessing.outliers_detection(dataset)

    def cleanup():
        dataset = Utils.load_csv(original_dataset_filename, include_cancelled=True)
        return dataset

    def reduce_size(dataset, factor=2):
        reduced_dataset = []
        for i in range(len(dataset)):
            if (i % factor == 0):
                reduced_dataset.append(dataset[i])
        return reduced_dataset

    def reduce_origin_airports_numbers(dataset, frequency_limit=500):
        new_dataset = []
        x = {}
        for i in range(len(dataset)):
            origin_airport_name = dataset[i].origin_airport_name
            if origin_airport_name not in x:
                x[origin_airport_name] = 0
            x[origin_airport_name] += 1
        keys_to_delete = []
        for key in x:
            if x[key] <= frequency_limit:
                keys_to_delete.append(key)
        for i in range(len(keys_to_delete)):
            x.pop(keys_to_delete[i], None)
        print(x)
        for i in range(len(dataset)):
            origin_airport = dataset[i].origin_airport_name
            if origin_airport in x:
                new_dataset.append(dataset[i])
        print(new_dataset)
        return new_dataset

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

    def outliers_detection(dataset):
        distance_values = []
        elapsed_time_values = []
        for i in range(len(dataset)):
            distance_values.append(float(dataset[i].distance))
            elapsed_time_values.append(float(dataset[i].elapsed_time))
        distance_mean = Utils.mean(distance_values)
        distance_stdev = Utils.stdev(distance_values)

        distance_values = np.array(sorted(distance_values))
        plt.figure()
        plt.boxplot([elapsed_time_values])
        plt.show()

    def create_processed_dataset(dataset, filename):
        dataset_list = []
        for i in range(len(dataset)):
            dataset_list.append(dataset[i].get_all_property_array())
        wr = csv.writer(open(filename, "w+"))
        wr.writerows(dataset_list)

DatasetProcessing().process_datasets()