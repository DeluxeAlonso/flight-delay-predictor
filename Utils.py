import csv
import math
import datetime
import pandas as pd
from Models.Flight import Flight

feature_engineering = 1 # 0:Holiday, 1:Days to holiday

class Utils:
    def load_csv(filename, include_cancelled=False):
        lines = csv.reader(open(filename, "r"))
        next(lines)
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            estimated_departure_time = dataset[i][14]
            real_departure_time = dataset[i][15]
            floating_point_pos = real_departure_time.find('.')
            if floating_point_pos != -1:
                real_departure_time = real_departure_time[0:floating_point_pos]
                dataset[i][15] = real_departure_time
            elapsed_time = dataset[i][22]
            tail_number = dataset[i][8]
            if include_cancelled:
                dataset_has_time_data = (len(estimated_departure_time) >= 1) and \
                                             (real_departure_time == '' or len(real_departure_time) >= 1)
            else:
                dataset_has_time_data = len(estimated_departure_time) >= 1 and \
                                             len(real_departure_time) >= 1
            dataset_has_missing_data = elapsed_time == '' or tail_number == ''
            if dataset_has_time_data and not dataset_has_missing_data:
                proccessed_dataset.append(Flight(dataset[i][1], dataset[i][2],
                                                 dataset[i][3], dataset[i][4],
                                                 dataset[i][5], dataset[i][6],
                                                 dataset[i][7], dataset[i][8],
                                                 dataset[i][9], dataset[i][10],
                                                 dataset[i][11], dataset[i][12],
                                                 dataset[i][13], dataset[i][14],
                                                 dataset[i][15], dataset[i][22],
                                                 dataset[i][23]))
        return proccessed_dataset

    def load_processed_dataset(filename):
        lines = csv.reader(open(filename, "r"))
        dataset = list(lines)
        proccessed_dataset = []
        for i in range(len(dataset)):
            flight = Flight(dataset[i][0], dataset[i][1],
                                dataset[i][2], dataset[i][3],
                                dataset[i][4], dataset[i][5],
                                dataset[i][6], dataset[i][7],
                                dataset[i][8], dataset[i][9],
                                dataset[i][10], dataset[i][11],
                                dataset[i][12], dataset[i][13],
                                dataset[i][14], dataset[i][15],
                                dataset[i][16])
            if dataset[i][17] is not None:
                if feature_engineering == 0:
                    flight.holiday = dataset[i][17]
                else:
                    flight.days_to_holiday = dataset[i][17]
            proccessed_dataset.append(flight)
        return proccessed_dataset

    # Files Handler

    def merge_csv_files(file_prefix, month_labels, output_filename):
        results = pd.read_csv(file_prefix + month_labels[0] + ".csv").dropna(how='all')
        for i in range(1, len(month_labels)):
            namedf = pd.read_csv(file_prefix + month_labels[i] + ".csv").dropna(how='all')
            results = results.append(namedf)
        results.to_csv(output_filename, encoding='utf-8')

    # Date Helpers

    def get_prior_day_date(day, month, year):
        string_date = Utils.get_date_string(day, month, year)
        date = datetime.datetime.strptime(string_date, "%d/%m/%Y").date()
        date = date + datetime.timedelta(days=-1)
        return date.strftime('%d/%m/%Y')

    def get_posterior_day_date(day, month, year):
        string_date = Utils.get_date_string(day, month, year)
        date = datetime.datetime.strptime(string_date, "%d/%m/%Y").date()
        date = date + datetime.timedelta(days=1)
        return date.strftime('%d/%m/%Y')

    def get_date(day, month, year):
        string_date = Utils.get_date_string(day, month, year)
        date = datetime.datetime.strptime(string_date, "%d/%m/%Y").date()
        return date.strftime('%d/%m/%Y')

    def get_date_string(day, month, year):
        return day + '/' + month + '/' + year

    def get_near_dates(day, month, year, include_current=False):
        if day == '1' and month == '1':
            post_date = Utils.get_posterior_day_date(day, month, year)
            prior_date = post_date
        elif day == '31' and month == '12':
            prior_date = Utils.get_prior_day_date(day, month, year)
            post_date = prior_date
        else:
            prior_date = Utils.get_prior_day_date(day, month, year)
            post_date = Utils.get_posterior_day_date(day, month, year)
        if include_current:
            current = Utils.get_date(day, month, year)
            return prior_date, current, post_date
        return  prior_date, post_date

    def days_difference_between_dates(first_date, second_date):
        f_date = datetime.datetime.strptime(first_date, "%d/%m/%Y").date()
        s_date = datetime.datetime.strptime(second_date, "%d/%m/%Y").date()
        delta = s_date - f_date
        return delta.days

    # Math

    def mean(values):
        return sum(values) / float(len(values))

    def stdev(values):
        avg = Utils.mean(values)
        variance = sum([pow(x - avg, 2) for x in values]) / float(len(values) - 1)
        return math.sqrt(variance)