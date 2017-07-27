import pandas as pd
import numpy as np
from Utils import  Utils
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier

class FeatureSelection:
    def univariate_selection(self):
        training_filename = 'Datasets/NaiveBayesDataset.csv'
        training_dataset = Utils.load_processed_dataset(training_filename)
        attributes_property_length = len(training_dataset[0].get_random_forest_property_array()) - 1
        df = FeatureSelection.get_property_data_frame(training_dataset, one_hot_encoding=True)
        array = df.values
        X = array[:, 0:attributes_property_length]
        Y = array[:, attributes_property_length]
        # feature extraction
        test = SelectKBest(score_func=chi2, k=4)
        fit = test.fit(X, Y)
        # summarize scores
        np.set_printoptions(precision=3)
        print(fit.scores_)

    def recursive_feature_elimination(self):
        training_filename = 'Datasets/NaiveBayesDataset.csv'
        training_dataset = Utils.load_processed_dataset(training_filename)
        attributes_property_length = len(training_dataset[0].get_random_forest_property_array()) - 1
        df = FeatureSelection.get_property_data_frame(training_dataset, one_hot_encoding=True)
        array = df.values
        X = array[:, 0:attributes_property_length]
        Y = array[:, attributes_property_length]
        # feature extraction
        model = LogisticRegression()
        rfe = RFE(model, 3)
        fit = rfe.fit(X, Y)
        print("Num Features: {0}".format(fit.n_features_))
        print("Selected Features: {}".format(fit.support_))
        print("Feature Ranking: {}".format(fit.ranking_))

    def feature_importance(self):
        training_filename = 'Datasets/NaiveBayesDataset.csv'
        training_dataset = Utils.load_processed_dataset(training_filename)
        attributes_property_length = len(training_dataset[0].get_random_forest_property_array()) - 1
        df = FeatureSelection.get_property_data_frame(training_dataset, one_hot_encoding=True)
        array = df.values
        X = array[:, 0:attributes_property_length]
        Y = array[:, attributes_property_length]
        # feature extraction
        model = ExtraTreesClassifier()
        model.fit(X, Y)
        print(model.feature_importances_)

    def get_property_data_frame(dataset, one_hot_encoding=False):
        attributes_array = []
        for i in range(len(dataset)):
            attributes_array.append(dataset[i].get_random_forest_property_array())
        df = pd.DataFrame(attributes_array)
        if one_hot_encoding:
            df = pd.get_dummies(df, drop_first=False)
        return df

FeatureSelection().feature_importance()