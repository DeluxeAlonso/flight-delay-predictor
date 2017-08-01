import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import pandas as pd

class EvaluationMeasure:

    def get_classifier_outcomes(test_set, predictions):
        tp, fp, tn, fn = 0, 0, 0, 0
        for x in range(len(test_set)):
            if test_set[x].get_numerical_property_array()[-1] == predictions[x] == 1:
                tp += 1
        for x in range(len(test_set)):
            if predictions[x] == 1 and test_set[x].get_numerical_property_array()[-1] != predictions[x]:
                fp += 1
        for x in range(len(test_set)):
            if test_set[x].get_numerical_property_array()[-1] == predictions[x] == 0:
                tn += 1
        for x in range(len(test_set)):
            if predictions[x] == 0 and test_set[x].get_numerical_property_array()[-1] != predictions[x]:
                fn += 1
        return tp, fp, tn, fn

    def show_evaluation_measure_values(test_set, predictions):
        tp, fp, tn, fn = EvaluationMeasure.get_classifier_outcomes(test_set, predictions)
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

    def get_test_set_values(test_set):
        test_values = []
        for result in map(lambda x: x.get_numerical_property_array()[-1], test_set):
            test_values.append(result)
        return test_values

    def show_roc_curve(test_set, probabilities):
        test_values = EvaluationMeasure.get_test_set_values(test_set)
        false_positive_rate, true_positive_rate, thresholds = roc_curve(test_values, probabilities)
        roc_auc = auc(false_positive_rate, true_positive_rate)
        plt.title('Receiver Operating Characteristic')
        plt.plot(false_positive_rate, true_positive_rate, 'b',
                 label='AUC = %0.2f' % roc_auc)
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([-0.1, 1.2])
        plt.ylim([-0.1, 1.2])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show()

    def show_confussion_matrix(test_set, predictions):
        test_values = EvaluationMeasure.get_test_set_values(test_set)
        y_actual = pd.Series(test_values, name ='Actual')
        y_pred = pd.Series(predictions, name = 'Predicted')
        df_confusion = pd.crosstab(y_actual, y_pred)
        print(df_confusion)
        EvaluationMeasure.plot_confusion_matrix(df_confusion, normalized=False)

    def plot_confusion_matrix(df_confusion, normalized = False, title='Matriz de confusión', cmap=plt.cm.gray_r):
        if normalized:
            df_confusion = df_confusion / df_confusion.sum(axis=1)
        plt.matshow(df_confusion, cmap=cmap)
        plt.colorbar()
        tick_marks = np.arange(len(df_confusion.columns))
        plt.xticks(tick_marks, df_confusion.columns, rotation=45)
        plt.yticks(tick_marks, df_confusion.index)
        plt.ylabel(df_confusion.index.name)
        plt.xlabel(df_confusion.columns.name)
        plt.show()