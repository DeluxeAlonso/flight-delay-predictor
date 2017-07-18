import csv
import math
import matplotlib.pyplot as plt
from Models.Flight import Flight

class Solver:
    def load_csv(filename):
        lines = csv.reader(open(filename, "r"))
        next(lines)
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            dataset_has_completed_data = dataset[i][9] != ''
            if dataset_has_completed_data:
                proccessed_dataset.append(Flight(dataset[i][0], dataset[i][1],
                                    dataset[i][2], dataset[i][3],
                                    dataset[i][4], dataset[i][5],
                                    dataset[i][8], dataset[i][9]))
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

    def calculate_probability(x, mean, stdev):
        #print("stdev {0}".format(stdev))
        exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
        return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

    def calculate_class_probabilities(summaries, input_vector, prior_probability):
        probabilities = {}
        for classValue, classSummaries in summaries.items():
            probabilities[classValue] = 1
            for i in range(len(classSummaries)):
                mean, stdev = classSummaries[i]
                x = input_vector[i]
                probabilities[classValue] *= Solver.calculate_probability(x, mean, stdev)
            #probabilities[classValue] *= 1.0 - prior_probability
        return probabilities

    def predict(summaries, input_vector, prior_probability):
        probabilities = Solver.calculate_class_probabilities(summaries, input_vector, prior_probability)
        bestLabel, bestProb = None, -1
        for classValue, probability in probabilities.items():
            if bestLabel is None or probability > bestProb:
                bestProb = probability
                bestLabel = classValue
        return bestLabel

    def get_predictions(summaries, test_set, prior_probability):
        predictions = []
        for i in range(len(test_set)):
            result = Solver.predict(summaries, test_set[i].get_property_array(), prior_probability)
            predictions.append(result)
        return predictions

    def get_accuracy(testSet, predictions):
        correct = 0
        for x in range(len(testSet)):
            if testSet[x].get_property_array()[-1] == predictions[x]:
                correct += 1
        return (correct / float(len(testSet))) * 100.0

    def show_roc_curve(test_set, predictions):
        tp, fp, tn, fn = 0, 0, 0, 0
        for x in range(len(test_set)):
            if test_set[x].get_property_array()[-1] == predictions[x] == 1:
                tp += 1
        for x in range(len(test_set)):
            if predictions[x] == 1 and test_set[x].get_property_array()[-1] != predictions[x]:
                fp += 1
        for x in range(len(test_set)):
            if test_set[x].get_property_array()[-1] == predictions[x] == 0:
                tn += 1
        for x in range(len(test_set)):
            if predictions[x] == 0 and test_set[x].get_property_array()[-1] != predictions[x]:
                fn += 1
        print("TP: {0}, FP: {1}, TN: {2}, FN: {3}".format(tp, fp, tn, fn))