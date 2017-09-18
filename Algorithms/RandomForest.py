import csv
import math
import pandas as pd
import numpy as np
import h2o
from h2o.grid import H2OGridSearch
from h2o.estimators import H2ORandomForestEstimator
from Models.Flight import Flight
import matplotlib.pyplot as plt

seed = 7
num_trees = 15
max_features = 8
n_splits = 3
max_depth = 20

class RandomForest:
    def get_property_data_frame(dataset, one_hot_encoding = False):
        attributes_array = []
        for i in range(len(dataset)):
            attributes_array.append(dataset[i].get_random_forest_property_array())
        df = pd.DataFrame(attributes_array)
        if one_hot_encoding:
            df = pd.get_dummies(df, drop_first=False)
        return df

    def get_h2o_predictions(training_dataset, testing_dataset, attribute_property_length):
        training_df = RandomForest.get_property_data_frame(training_dataset, one_hot_encoding=False)
        testing_df = RandomForest.get_property_data_frame(testing_dataset, one_hot_encoding=False)
        h2o.init()
        h2o.connect()
        training_array = training_df.values
        testing_array = testing_df.values
        x = training_array[:, 0:attribute_property_length]
        y = training_array[:, attribute_property_length - 1]

        x_test = testing_array[:, 0:attribute_property_length]
        ts_df = h2o.H2OFrame(x_test)
        tr_df = h2o.H2OFrame(x)

        training_columns = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7','C8', 'C9', 'C10',
                            'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19',
                            'C20', 'C21', 'C22', 'C23']
        response_column = 'C24'
        model = H2ORandomForestEstimator(ntrees=num_trees, max_depth=max_depth, nfolds=n_splits)
        model.train(x=training_columns, y=response_column, training_frame=tr_df, validation_frame=ts_df)
        predictions = model.predict(ts_df)
        model.show()
        print(model.varimp(True))
        predictions_array = []
        probabilities_array = []
        predictions = predictions.as_data_frame().values.tolist()
        for i in range(len(predictions)):
            if predictions[i][0] >= 0.5:
                predictions_array.append(1.0)
            else:
                predictions_array.append(0.0)
            probabilities_array.append(predictions[i][0])
        return predictions_array, probabilities_array

    def grid_search(training_df, attribute_property_length):
        h2o.init()
        h2o.connect()
        training_array = training_df.values
        x = training_array[:, 0:attribute_property_length]
        y = training_array[:, attribute_property_length - 1]
        tr_df = h2o.H2OFrame(x)
        training_columns = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
                            'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19',
                            'C20', 'C21', 'C22', 'C23']
        response_column = 'C24'
        hyper_parameters = {'ntrees': [20, 25], 'max_depth': [45, 50, 55]}
        random_plus_manual = H2OGridSearch(H2ORandomForestEstimator(nfolds=n_splits), hyper_parameters)
        random_plus_manual.train(x=training_columns, y=response_column, training_frame=tr_df)
        random_plus_manual.show()