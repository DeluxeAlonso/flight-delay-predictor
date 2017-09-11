from Algorithms.NaiveBayes import NaiveBayes
from Algorithms.RandomForest import RandomForest
from DataExploration import DataExploration as expl
from EvaluationMeasure import EvaluationMeasure as eval
from Utils import Utils, FeatureEngineering

original_training_filename = 'Datasets/NewYork/Training/merged_training.csv'
training_filename = 'Datasets/TrainingDataset.csv'
testing_filename = 'Datasets/TestingDataset.csv'

class Main:
    def naive_bayes_predictor(self):
        training_dataset = Utils.load_processed_dataset(training_filename, include_weather=True)
        testing_dataset = Utils.load_processed_dataset(testing_filename, include_weather=True)
        # Model preparation
        separated_training_dataset = NaiveBayes.separate_by_class(training_dataset, 0)
        prior_probability = len(separated_training_dataset[0]) / (len(training_dataset))
        numerical_summaries = NaiveBayes.summarize_numerical_values_by_class(separated_training_dataset)
        categorical_summaries = NaiveBayes.summarize_categorical_values_by_class(training_dataset)
        summaries = [numerical_summaries, categorical_summaries]
        # Model testing
        predictions, probabilities = NaiveBayes.get_predictions(summaries, testing_dataset, prior_probability)
        eval.show_evaluation_measure_values(testing_dataset, predictions)
        eval.show_all_evaluation_graphics(testing_dataset, probabilities, predictions)

    def random_forest_grid_search(self):
        training_dataset = Utils.load_processed_dataset(training_filename)
        training_df = RandomForest.get_property_data_frame(training_dataset)
        random_forest_property_length = len(training_dataset[0].get_random_forest_property_array())
        RandomForest.grid_search(training_df, random_forest_property_length)

    def random_forest_predictor(self):
        training_dataset = Utils.load_processed_dataset(training_filename, include_weather=True)
        testing_dataset = Utils.load_processed_dataset(testing_filename, include_weather=True)
        random_forest_property_length = len(training_dataset[0].get_random_forest_property_array())
        predictions, probabilities = RandomForest.get_h2o_predictions(training_dataset, testing_dataset,
                                                   random_forest_property_length)
        eval.show_evaluation_measure_values(testing_dataset, predictions)
        eval.show_all_evaluation_graphics(testing_dataset, probabilities, predictions)

    def data_exploration(self):
        dataset = Utils.load_processed_dataset(training_filename, include_weather=True)
        separated_dataset = NaiveBayes.separate_by_class(dataset, 0)
        print('Separated instances: {0}'.format(separated_dataset))
        print('First row data date: {0}'.format(dataset[0].get_numerical_property_array()))
        print('Loaded data file {0} with {1} rows'.format(training_filename, len(dataset)))
        print('Number of delayes flights {0}'.format(len(separated_dataset[1])))
        expl.show_delays_per_raining_day(dataset)

    def data_analysis(self):
        expl.show_basic_information(training_filename)

Main().naive_bayes_predictor()