import csv
import math
import pandas as pd
import numpy as np
import h2o
from h2o.estimators import H2ORandomForestEstimator
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from Models.Flight import Flight
import matplotlib.pyplot as plt

seed = 7
num_trees = 50
max_features = 8
n_splits = 5

class RandomForest:
    def load_csv(filename):
        lines = csv.reader(open(filename, "r"))
        next(lines)
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            should_avoid = dataset[i][-1] == 0.0 and ((i % 2 == 0) )
            dataset_has_completed_data = len(dataset[i][11]) >=3 and len(dataset[i][12]) >= 3 and dataset[i][16] != ''
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

    def get_property_data_frame(dataset, one_hot_encoding = False):
        attributes_array = []
        for i in range(len(dataset)):
            attributes_array.append(dataset[i].get_random_forest_property_array())
        df = pd.DataFrame(attributes_array)
        if one_hot_encoding:
            df = pd.get_dummies(df, drop_first=False)
        return df

    def get_predictions(training_df, testing_df, attribute_property_length):
        training_array = training_df.values
        testing_array = testing_df.values
        x = training_array[:,0:attribute_property_length - 1]
        y = training_array[:,attribute_property_length - 1]
        x_test = testing_array[:,0:attribute_property_length - 1]
        model = RandomForestClassifier(n_estimators=num_trees, max_features=max_features)
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

    def get_cross_validation_accuracy(training_df, attribute_property_length):
        training_array = training_df.values
        x = training_array[:, 0:attribute_property_length]
        y = training_array[:, attribute_property_length]
        model = RandomForestClassifier(n_estimators=num_trees, max_features=max_features)
        kfold = model_selection.KFold(n_splits=n_splits, random_state=seed)
        results = model_selection.cross_val_score(model, x, y, cv=kfold)
        print(results)
        print(results.mean())

    def get_h2o_predictions(training_df, testing_df, attribute_property_length):
        h2o.init()
        h2o.connect()
        training_array = training_df.values
        testing_array = testing_df.values
        x = training_array[:, 0:attribute_property_length]
        y = training_array[:, attribute_property_length - 1]
        x_test = testing_array[:, 0:attribute_property_length]
        ts_df = h2o.H2OFrame(x_test)
        tr_df = h2o.H2OFrame(x)
        training_columns = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
        response_column = 'C9'
        model = H2ORandomForestEstimator(balance_classes=True, ntrees=num_trees, max_depth=20, nfolds=5)
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