import csv
import math
from Models.Flight import Flight

class Utils:
    def load_csv(filename, include_cancelled=False):
        lines = csv.reader(open(filename, "r"))
        next(lines)
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            if include_cancelled:
                dataset_has_completed_data = (len(dataset[i][11]) >= 3 and dataset[i][16] != '') and \
                                             (dataset[i][12] == '' or len(dataset[i][12]) >=3 and dataset[i][16] != '')
            else:
                dataset_has_completed_data = len(dataset[i][11]) >=3 and \
                                             len(dataset[i][12]) >=3 and dataset[i][16] != ''
            if dataset_has_completed_data:
                proccessed_dataset.append(Flight(dataset[i][0], dataset[i][1],
                                    dataset[i][2], dataset[i][3],
                                    dataset[i][4], dataset[i][5],
                                    dataset[i][6], dataset[i][7],
                                    dataset[i][8], dataset[i][9],
                                    dataset[i][10], dataset[i][11],
                                    dataset[i][12], dataset[i][16],
                                    dataset[i][17]))
        return proccessed_dataset

    def load_processed_dataset(filename):
        lines = csv.reader(open(filename, "r"))
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            proccessed_dataset.append(Flight(dataset[i][0], dataset[i][1],
                                dataset[i][2], dataset[i][3],
                                dataset[i][4], dataset[i][5],
                                dataset[i][6], dataset[i][7],
                                dataset[i][8], dataset[i][9],
                                dataset[i][10], dataset[i][11],
                                dataset[i][12], dataset[i][13],
                                dataset[i][14]))
        return proccessed_dataset

    def mean(values):
        return sum(values) / float(len(values))

    def stdev(values):
        avg = Utils.mean(values)
        variance = sum([pow(x - avg, 2) for x in values]) / float(len(values) - 1)
        return math.sqrt(variance)