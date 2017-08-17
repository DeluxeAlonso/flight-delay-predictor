import csv
import math
import pandas as pd
import numpy as np
import h2o
from h2o.grid import H2OGridSearch
from h2o.estimators import H2ORandomForestEstimator
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from Models.Flight import Flight
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer

seed = 7
num_trees = 25
max_features = 8
n_splits = 3

class RandomForest:
    def get_property_data_frame(dataset, one_hot_encoding = False):
        attributes_array = []
        for i in range(len(dataset)):
            attributes_array.append(dataset[i].get_random_forest_property_array())
        df = pd.DataFrame(attributes_array)
        if one_hot_encoding:
            df = pd.get_dummies(df, drop_first=False)
        return df

    def get_sklearn_predictions(training_dataset, testing_dataset, attribute_property_length):
        training_df = RandomForest.get_property_data_frame(training_dataset, one_hot_encoding=True)
        testing_df = RandomForest.get_property_data_frame(testing_dataset, one_hot_encoding=True)

        # get the columns in train that are not in test
        tr_columns = training_df.columns.values.tolist()
        ts_columns = testing_df.columns.values.tolist()
        col_to_add = list(set(tr_columns) - set(ts_columns))
        # add these columns to test, setting them equal to zero
        for c in col_to_add:
            testing_df[c] = 0
        # select and reorder the test columns using the train columns
        testing_df = testing_df[training_df.columns]

        training_array = training_df.values
        testing_array = testing_df.values
        class_column = 1
        print(len(training_array[0]))
        print(len(testing_array[0]))
        x = training_array[:, 0:len(training_array[0]) - 1]
        x = np.delete(x, class_column, 1)
        print(x)
        y = training_array[:, class_column]
        print(y)
        x_test = testing_array[:, 0:len(training_array[0]) - 1]
        x_test = np.delete(x_test, class_column, 1)

        #SMOTE ALGORITHM
        #sm = SMOTE(random_state=12, ratio=1.0)
        #x, y = sm.fit_sample(x, y)

        model = RandomForestClassifier(n_estimators=num_trees, max_features=None, max_depth=20)
        classifier = model.fit(x, y)
        predictions = classifier.predict_proba(x_test)
        predictions_array = []
        probabilities_array = []
        predictions = predictions.tolist()
        print(predictions)

        for i in range(len(predictions)):
            x = predictions[i][0]
            y = predictions[i][1]
            if x >= y:
                predictions_array.append(0.0)
            else:
                predictions_array.append(1.0)
            probabilities_array.append(y)
        return predictions_array, probabilities_array

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

        training_columns = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7','C8', 'C9']
        response_column = 'C10'
        model = H2ORandomForestEstimator(ntrees=num_trees, max_depth=20, nfolds=n_splits)
        model.train(x=training_columns, y=response_column, training_frame=tr_df, validation_frame=ts_df)
        predictions = model.predict(ts_df)
        model.show()
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
        training_columns = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']
        response_column = 'C11'
        hyper_parameters = {'ntrees': [5, 10, 20, 30],
                            'max_depth': [5, 10, 20, 30]}

        random_plus_manual = H2OGridSearch(H2ORandomForestEstimator(nfolds=5),
                      hyper_parameters,
                      grid_id="random_plus_manual")
        random_plus_manual.train(x=training_columns, y=response_column, training_frame=tr_df)
        random_plus_manual.show()