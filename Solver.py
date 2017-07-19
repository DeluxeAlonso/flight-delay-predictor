import csv
import math
import matplotlib.pyplot as plt
from Models.Flight import Flight

alpha = 1

class Solver:
    def load_csv(filename):
        lines = csv.reader(open(filename, "r"))
        next(lines)
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            dataset_has_completed_data = dataset[i][12] != ''
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

    def separate_by_class(dataset, type):
        separated = {}
        for i in range(len(dataset)):
            if type == 0:
                vector = dataset[i].get_numerical_property_array()
            else:
                vector = dataset[i].get_categorical_property_array()
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

    def get_categorical_values_frequency(values, data_count, vector_dimensionality):
        frequency = {}
        for i in range(len(values)):
            if (values[i] not in frequency):
                frequency[values[i]] = 0
            frequency[values[i]] += 1
        for key in frequency:
            frequency[key] = ( (frequency[key] + alpha) / (data_count + vector_dimensionality * alpha) )
        return frequency

    def summarize_categorical_values_by_class(dataset):
        summaries = {}
        separated_dataset = Solver.separate_by_class(dataset, 1)
        vector_dimensionality = len(dataset[0].get_categorical_property_array())
        for classValue, instances in separated_dataset.items():
            array = [(Solver.get_categorical_values_frequency(values,
                                                              len(separated_dataset[classValue]),
                                                              vector_dimensionality)) for values in zip(*instances)]
            del array[-1]
            summaries[classValue] = array
        return summaries

    def summarize_separated_dataset(separated_dataset):
        summaries = [(Solver.mean(attribute), Solver.stdev(attribute)) for attribute in zip(*separated_dataset)]
        del summaries[-1]
        return summaries

    def summarize_numerical_values_by_class(separated_dataset):
        summaries = {}
        for classValue, instances in separated_dataset.items():
            summaries[classValue] = Solver.summarize_separated_dataset(instances)
        return summaries

    def calculate_probability_density_function_value(x, mean, stdev):
        exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
        return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

    def calculate_class_probabilities(summaries, numerical_input_vector, categorical_input_vector, prior_probability):
        probabilities = {}
        # Numerical Attributes
        for classValue, classSummaries in summaries[0].items():
            probabilities[classValue] = 1
            for i in range(len(classSummaries)):
                mean, stdev = classSummaries[i]
                x = numerical_input_vector[i]
                probabilities[classValue] *= Solver.calculate_probability_density_function_value(x, mean, stdev)
        # Categorical Attributes
        for classValue, classSummaries in summaries[1].items():
            #probabilities[classValue] = 1
            for i in range(len(classSummaries)):
                frequency_dict = classSummaries[i]
                probability = 1
                x = categorical_input_vector[i]
                if x in frequency_dict:
                    probability = frequency_dict[x]
                probabilities[classValue] *= probability
            if classValue == 0.0:
                probabilities[classValue] *= prior_probability
            else:
                probabilities[classValue] *= 1.0 - prior_probability
        return probabilities

    def predict(summaries, numerical_input_vector, categorical_input_vector, prior_probability):
        probabilities = Solver.calculate_class_probabilities(summaries, numerical_input_vector,
                                                             categorical_input_vector, prior_probability)
        bestLabel, bestProb = None, -1
        for classValue, probability in probabilities.items():
            if bestLabel is None or probability > bestProb:
                bestProb = probability
                bestLabel = classValue
        return bestLabel

    def get_predictions(summaries, test_set, prior_probability):
        predictions = []
        for i in range(len(test_set)):
            result = Solver.predict(summaries, test_set[i].get_numerical_property_array(),
                                    test_set[i].get_categorical_property_array(), prior_probability)
            predictions.append(result)
        return predictions

    def get_accuracy(testSet, predictions):
        correct = 0
        for x in range(len(testSet)):
            if testSet[x].get_numerical_property_array()[-1] == predictions[x]:
                correct += 1
        return (correct / float(len(testSet))) * 100.0

    def get_classifier_outcomes(test_set, predictions):
        tp, fp, tn, fn = 0, 0, 0, 0
        for x in range(len(test_set)):
            if test_set[x].get_numerical_property_array()[-1] == predictions[x] == 1:
                tp += 1
        for x in range(len(test_set)):
            if predictions[x] == 1 and test_set[x].get_numerical_property_array()[-1] != predictions[x]:
                fp += 1
        for x in range(len(test_set)):
            if test_set[x].get_numerical_property_array()[-1] == predictions[x] == 0:
                tn += 1
        for x in range(len(test_set)):
            if predictions[x] == 0 and test_set[x].get_numerical_property_array()[-1] != predictions[x]:
                fn += 1
        return tp, fp, tn, fn

    def show_roc_curve(test_set, predictions):
        tp, fp, tn, fn = Solver.get_classifier_outcomes(test_set, predictions)
        print("TP: {0}, FP: {1}, TN: {2}, FN: {3}".format(tp, fp, tn, fn))

    def show_confussion_matrix(test_set, predictions):
        tp, fp, tn, fn = Solver.get_classifier_outcomes(test_set, predictions)
        print("TP: {0}, FP: {1}, TN: {2}, FN: {3}".format(tp, fp, tn, fn))
        sensitivity = tp / (tp + fn)
        specificity = tn / (tn + fp)
        precision = tp / (tp + fp)
        error_rate = (fp + fn) / (fp + fn + tp + tn)
        print("Sensitivity or Recall: {0}%".format(sensitivity * 100.00))
        print("Specificity: {0}%".format(specificity * 100.00))
        print("Precision: {0}%".format(precision * 100.00))
        print("Error rate: {0}%".format(error_rate * 100.00))