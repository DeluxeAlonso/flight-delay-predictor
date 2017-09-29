import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import h2o
from h2o.estimators import H2ORandomForestEstimator

training_filename = 'Datasets/TrainingCorpus.csv'
testing_filename = 'Datasets/TestingCorpus.csv'

model_filename = '/Users/Alonso/Documents/Tesis/FlightDelayPredictor/DRF_model_python_1506367636251_1'

num_trees = 60
max_depth = 20
n_splits = 3
threshold = 0.5

class AlogrithmicModel:
    def save_final_model(self):
        tr_df = pd.read_csv(training_filename)
        ts_df = pd.read_csv(testing_filename)

        tr_df[["DELAYED"]] = tr_df[["DELAYED"]].astype(int).astype(bool)
        ts_df[["DELAYED"]] = ts_df[["DELAYED"]].astype(int).astype(bool)

        cols = list(tr_df.columns.values)

        h2o.init()
        h2o.connect()

        training = h2o.H2OFrame(tr_df)
        test = h2o.H2OFrame(ts_df)

        target_column = cols[-1]
        training_columns = cols[:-1]

        model = H2ORandomForestEstimator(ntrees=num_trees, max_depth=max_depth, nfolds=n_splits)
        model.train(x=training_columns, y=target_column, training_frame=training, validation_frame=test)

        m = h2o.save_model(model=model, path="/", force=True)
        print(m)

    def load_final_model(self):
        tr_df = pd.read_csv(training_filename)
        ts_df = pd.read_csv(testing_filename)

        tr_df[["DELAYED"]] = tr_df[["DELAYED"]].astype(int).astype(bool)
        ts_df[["DELAYED"]] = ts_df[["DELAYED"]].astype(int).astype(bool)

        print(tr_df)

        cols = list(tr_df.columns.values)
        ytest = ts_df.values[:, len(cols) - 1]

        h2o.init()
        h2o.connect()
        test = h2o.H2OFrame(ts_df)

        print(test)

        model = h2o.load_model(model_filename)
        probabilities = model.predict(test)
        probabilities = probabilities.as_data_frame().values.tolist()
        probs_array = []
        pred_array = []
        for i in range(len(probabilities)):
            if probabilities[i][2] >= threshold:
                pred_array.append(1.0)
            else:
                pred_array.append(0.0)
            probs_array.append(probabilities[i][2])
        AlogrithmicModel.show_measure_metrics(pred_array, ytest)

    def show_measure_metrics(pred_array, ytest):
        tp, fp, tn, fn = 0, 0, 0, 0
        for x in range(len(ytest)):
            if ytest[x] == pred_array[x] == 1:
                tp += 1
        for x in range(len(ytest)):
            if pred_array[x] == 1 and ytest[x] != pred_array[x]:
                fp += 1
        for x in range(len(ytest)):
            if ytest[x] == pred_array[x] == 0:
                tn += 1
        for x in range(len(ytest)):
            if pred_array[x] == 0 and ytest[x] != pred_array[x]:
                fn += 1

        sensitivity = tp / (tp + fn)  # the fraction of positives that are correctly classified
        specificity = tn / (tn + fp)  # the fraction of negatives that are correctly classified
        precision = tp / (tp + fp)
        error_rate = (fp + fn) / (fp + fn + tp + tn)
        accuracy = 1.0 - error_rate
        f_score = (2 * precision * sensitivity) / (precision + sensitivity)
        print("TP: {0}, FP: {1}, TN: {2}, FN: {3}".format(tp, fp, tn, fn))
        print("Sensitivity or Recall: {0}%".format(sensitivity * 100.00))
        print("Specificity: {0}%".format(specificity * 100.00))
        print("Precision: {0}%".format(precision * 100.00))
        print("Error rate: {0}%".format(error_rate * 100.00))
        print("Accuracy: {0}%".format(accuracy * 100.00))
        print("F1 Score: {0}%".format(f_score))

    def evaluate_instance(df):
        test = h2o.H2OFrame(df)

        model = h2o.load_model(model_filename)
        probabilities = model.predict(test)
        probabilities = probabilities.as_data_frame().values.tolist()
        return probabilities[0][2]

AlogrithmicModel().load_final_model()