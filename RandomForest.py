import csv
import math
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from Models.Flight import Flight

seed = 7
num_trees = 50
max_features = 3
n_splits = 5

class RandomForest:
    def load_csv(filename):
        lines = csv.reader(open(filename, "r"))
        next(lines)
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            should_avoid = not (i % 5 == 0)
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

    def get_property_data_frame(dataset):
        attributes_array = []
        for i in range(len(dataset)):
            attributes_array.append(dataset[i].get_random_forest_property_array())
        df = pd.DataFrame(attributes_array)
        one_hot_encoded_df = pd.get_dummies(df, drop_first=False)
        return one_hot_encoded_df

    def get_predictions(training_df, testing_df, attribute_property_length):
        training_array = training_df.values
        testing_array = testing_df.values
        x = training_array[:,0:attribute_property_length]
        y = training_array[:,attribute_property_length]
        x_test = testing_array[:,0:attribute_property_length]
        model = RandomForestClassifier(n_estimators=num_trees, max_features=max_features)
        classifier = model.fit(x, y)
        predictions = classifier.predict_proba(x_test)
        predictions_array = []
        probabilities_array = []
        predictions = predictions.tolist()
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