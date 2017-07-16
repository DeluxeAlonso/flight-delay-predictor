import csv
import math
from Models.Flight import Flight

class Solver:
    def load_csv(filename):
        lines = csv.reader(open(filename, "r"))
        next(lines)
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            dataset_has_completed_data = dataset[i][7] != ''
            if dataset_has_completed_data:
                proccessed_dataset.append(Flight(dataset[i][0], dataset[i][1],
                                    dataset[i][2], dataset[i][3],
                                    dataset[i][6], dataset[i][7]))
        return proccessed_dataset

    def separate_by_class(dataset):
        separated = {}
        for i in range(len(dataset)):
            vector = dataset[i].get_property_array()
            if (vector[-1] not in separated):
                separated[vector[-1]] = []
            separated[vector[-1]].append(vector)
        return separated

    def mean(values):
        return sum(values) / float(len(values))

    def stdev(values):
        avg = Solver.mean(values)
        variance = sum([pow(x - avg, 2) for x in values]) / float(len(values) - 1)
        return math.sqrt(variance)

    def summarize(dataset):
        mapped_dataset = list(map((lambda x: x.get_property_array()), dataset))
        summaries = [(Solver.mean(attribute), Solver.stdev(attribute)) for attribute in zip(*mapped_dataset)]
        del summaries[-1]
        return summaries

    def summarize_separated_dataset(separated_dataset):
        summaries = [(Solver.mean(attribute), Solver.stdev(attribute)) for attribute in zip(*separated_dataset)]
        del summaries[-1]
        return summaries

    def summarize_by_class(separated_dataset):
        summaries = {}
        for classValue, instances in separated_dataset.items():
            summaries[classValue] = Solver.summarize_separated_dataset(instances)
        return summaries
