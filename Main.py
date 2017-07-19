import numpy as np
import matplotlib.pyplot as plt
from Solver import Solver
from DataExploration import DataExploration as expl
from Models.Flight import Flight

class Main:
    def load_data(self):
        training_filename = 'Datasets/NewYork/training.csv'
        testing_filename = 'Datasets/NewYork/testing.csv'
        training_dataset = Solver.load_csv(training_filename)
        testing_dataset = Solver.load_csv(testing_filename)
        #Model preparation
        separated_training_dataset = Solver.separate_by_class(training_dataset, 0)
        prior_probability = len(separated_training_dataset[0]) / (len(training_dataset))
        numerical_summaries = Solver.summarize_numerical_values_by_class(separated_training_dataset)
        categorical_summaries = Solver.summarize_categorical_values_by_class(training_dataset)
        summaries = [numerical_summaries, categorical_summaries]
        print(summaries)
        #Model testing
        predictions = Solver.get_predictions(summaries, testing_dataset, prior_probability)
        accuracy = Solver.get_accuracy(testing_dataset, predictions)
        Solver.show_roc_curve(testing_dataset, predictions)
        print('Accuracy: {0}%'.format(accuracy))
        print(prior_probability)

    def data_exploration(self):
        filename = 'Datasets/NewYork/testing.csv'
        dataset = Solver.load_csv(filename)
        separated_dataset = Solver.separate_by_class(dataset, 0)
        print('Separated instances: {0}'.format(separated_dataset))
        print('First row data date: {0}'.format(dataset[0].get_numerical_property_array()))
        print('Loaded data file {0} with {1} rows'.format(filename, len(dataset)))
        print('Number of delayes flights {0}'.format(len(separated_dataset[1])))
        expl.show_delays_per_month(dataset)

Main().load_data()