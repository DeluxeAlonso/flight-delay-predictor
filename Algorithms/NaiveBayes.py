import csv
import math
from Utils import Utils
from Models.Flight import Flight

alpha = 1.0

class NaiveBayes:
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

    def get_numerical_mean_stdev(separated_dataset):
        summaries = [(Utils.mean(attribute), Utils.stdev(attribute)) for attribute in zip(*separated_dataset)]
        del summaries[-1]
        return summaries

    def get_categorical_values_frequency(values, data_count, features_dimensionality):
        frequency = {}
        for i in range(len(values)):
            if (values[i] not in frequency):
                frequency[values[i]] = 0
            frequency[values[i]] += 1
        for key in frequency:
            frequency[key] = ( (frequency[key] + alpha) / (data_count + features_dimensionality * alpha) )
        frequency["-1"] = (alpha / (data_count + features_dimensionality * alpha))
        return frequency

    def summarize_categorical_values_by_class(dataset):
        summaries = {}
        separated_dataset = NaiveBayes.separate_by_class(dataset, 1)
        features_dimensionality = len(dataset[0].get_categorical_property_array()) \
                                + len(dataset[0].get_numerical_property_array()) - 2
        for classValue, instances in separated_dataset.items():
            array = [(NaiveBayes.get_categorical_values_frequency(values,
                                                                  len(separated_dataset[classValue]),
                                                                  features_dimensionality)) for values in zip(*instances)]
            del array[-1]
            summaries[classValue] = array
        return summaries

    def summarize_numerical_values_by_class(separated_dataset):
        summaries = {}
        for classValue, instances in separated_dataset.items():
            summaries[classValue] = NaiveBayes.get_numerical_mean_stdev(instances)
        return summaries

    def calculate_probability_density_function_value(x, mean, stdev):
        if x is None:
            x = 0.0
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
                probabilities[classValue] *= NaiveBayes.calculate_probability_density_function_value(x, mean, stdev)
        # Categorical Attributes
        for classValue, classSummaries in summaries[1].items():
            for i in range(len(classSummaries)):
                frequency_dict = classSummaries[i]
                x = categorical_input_vector[i]
                if x in frequency_dict:
                    probability = frequency_dict[x]
                else:
                    probability = frequency_dict["-1"]
                probabilities[classValue] *= probability
            if classValue == 0.0:
                probabilities[classValue] *= prior_probability
            else:
                probabilities[classValue] *= 1.0 - prior_probability
        normalized_prob = probabilities[1.0]/(probabilities[0.0] + probabilities[1.0])
        return probabilities, normalized_prob

    def predict(summaries, numerical_input_vector, categorical_input_vector, prior_probability):
        probabilities, normalized_prob = NaiveBayes.calculate_class_probabilities(summaries, numerical_input_vector,
                                                                 categorical_input_vector, prior_probability)
        bestLabel, bestProb = None, -1
        for classValue, probability in probabilities.items():
            if bestLabel is None or probability > bestProb:
                bestProb = probability
                bestLabel = classValue
        return bestLabel, normalized_prob

    def get_predictions(summaries, test_set, prior_probability):
        predictions = []
        probabilities = []
        for i in range(len(test_set)):
            result, prob = NaiveBayes.predict(summaries, test_set[i].get_numerical_property_array(),
                                        test_set[i].get_categorical_property_array(), prior_probability)
            predictions.append(result)
            probabilities.append(prob)
        return predictions, probabilities
