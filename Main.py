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
        separated_training_datase = Solver.separate_by_class(training_dataset)
        summaries = Solver.summarize_by_class(separated_training_datase)
        print(summaries)
        #Model testing
        predictions = Solver.get_predictions(summaries, testing_dataset)
        accuracy = Solver.get_accuracy(testing_dataset, predictions)
        print('Accuracy: {0}%'.format(accuracy))

    def data_exploration(self):
        filename = 'Datasets/NewYork/training.csv'
        dataset = Solver.load_csv(filename)
        separated_dataset = Solver.separate_by_class(dataset)
        summary = Solver.summarize(dataset)
        separated_sumary = Solver.summarize_by_class(separated_dataset)
        print('Separated instances: {0}'.format(separated_dataset))
        print('First row data date: {0}'.format(dataset[0].get_property_array()))
        print('Attribute summaries: {0}'.format(summary))
        print('Attribute summaries by classes: {0}'.format(separated_sumary))
        print('Loaded data file {0} with {1} rows'.format(filename, len(dataset)))
        print('Number of delayes flights {0}'.format(len(separated_dataset[1])))
        expl.show_delays_per_month(dataset)

Main().data_exploration()