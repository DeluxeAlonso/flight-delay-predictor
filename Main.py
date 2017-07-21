import numpy as np
import matplotlib.pyplot as plt
from NaiveBayes import NaiveBayes
from RandomForest import RandomForest
from DataExploration import DataExploration as expl
from EvaluationMeasure import  EvaluationMeasure as eval
from Models.Flight import Flight

class Main:

    def naive_bayes_predictor(self):
        training_filename = 'Datasets/NewYork/training.csv'
        testing_filename = 'Datasets/NewYork/testing.csv'
        training_dataset = NaiveBayes.load_csv(training_filename)
        testing_dataset = NaiveBayes.load_csv(testing_filename)
        # Model preparation
        separated_training_dataset = NaiveBayes.separate_by_class(training_dataset, 0)
        prior_probability = len(separated_training_dataset[0]) / (len(training_dataset))
        numerical_summaries = NaiveBayes.summarize_numerical_values_by_class(separated_training_dataset)
        categorical_summaries = NaiveBayes.summarize_categorical_values_by_class(training_dataset)
        summaries = [numerical_summaries, categorical_summaries]
        # Model testing
        predictions = NaiveBayes.get_predictions(summaries, testing_dataset, prior_probability)
        eval.show_evaluation_measure_values(testing_dataset, predictions)
        eval.show_confussion_matrix(testing_dataset, predictions)

    def random_forest_predictor(self):
        training_filename = 'Datasets/NewYork/training.csv'
        testing_filename = 'Datasets/NewYork/testing.csv'
        training_dataset = RandomForest.load_csv(training_filename)
        testing_dataset = RandomForest.load_csv(testing_filename)
        training_df = RandomForest.get_property_data_frame(training_dataset)
        testing_df = RandomForest.get_property_data_frame(testing_dataset)
        random_forest_property_length = len(training_dataset[0].get_random_forest_property_array())
        predictions, probabilities = RandomForest.get_h2o_predictions(training_df, testing_df,
                                                   random_forest_property_length)
        eval.show_evaluation_measure_values(testing_dataset, predictions)
        eval.show_roc_curve(testing_dataset, probabilities)

    def data_exploration(self):
        filename = 'Datasets/NewYork/training.csv'
        dataset = NaiveBayes.load_csv(filename)
        separated_dataset = NaiveBayes.separate_by_class(dataset, 0)
        print('Separated instances: {0}'.format(separated_dataset))
        print('First row data date: {0}'.format(dataset[0].get_numerical_property_array()))
        print('Loaded data file {0} with {1} rows'.format(filename, len(dataset)))
        print('Number of delayes flights {0}'.format(len(separated_dataset[1])))
        expl.show_delays_per_month(dataset)

Main().data_exploration()