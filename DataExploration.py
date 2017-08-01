import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

n_months = 12
n_days_per_week = 7
bar_width = 0.35

class DataExploration:
    def show_basic_information(filename):
        dataset = pd.read_csv(filename)
        print(dataset.head())
        print(dataset.shape)
        for col in dataset:
            print("%d NULL values are found in column %s" % (dataset[col].isnull().sum().sum(), col))
        print(dataset.columns.values)

    def show_delays_per_month(dataset):
        x = [0] * n_months
        y = [0] * n_months
        for i in range(len(dataset)):
            property_array = dataset[i].get_categorical_property_array()
            index = int(property_array[0]) - 1
            y[index] += 1
            if property_array[-1] == 1.0:
                x[index] += 1
        ind = np.arange(n_months)
        fig, ax = plt.subplots()
        delayed_flights_tuple, total_flights_tuple = DataExploration.generate_flight_bar_tuples(x, y, n_months)
        delayed_flights_bar = ax.bar(ind, delayed_flights_tuple, bar_width, color='r')
        total_flights_bar = ax.bar(ind + bar_width, total_flights_tuple, bar_width, color='y')
        ax.set_ylabel('Cantidad de viajes')
        ax.set_title('Viajes retrasados')
        ax.set_xticks(ind + bar_width / 2)
        ax.set_xticklabels(('ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'))
        ax.legend((delayed_flights_bar[0], total_flights_bar[0]), ('Viajes retrasados', 'Viajes totales'))
        plt.show()

    def generate_flight_bar_tuples(x, y, max_range):
        delayed_flights = ()
        total_flights = ()
        for i in range(max_range):
            delayed_flights += (x[i],)
            total_flights += (y[i],)
        return delayed_flights, total_flights

    def show_delays_per_day_of_week(dataset):
        x = [0] * n_days_per_week
        y = [0] * n_days_per_week
        for i in range(len(dataset)):
            property_array = dataset[i].get_categorical_property_array()
            index = int(property_array[2]) - 1
            y[index] += 1
            if property_array[-1] == 1.0:
                x[index] += 1
        ind = np.arange(n_days_per_week)
        fig, ax = plt.subplots()
        delayed_flights_tuple, total_flights_tuple = DataExploration.generate_flight_bar_tuples(x, y, n_days_per_week)
        delayed_flights_bar = ax.bar(ind, delayed_flights_tuple, bar_width, color='r')
        total_flights_bar = ax.bar(ind + bar_width, total_flights_tuple, bar_width, color='y')
        ax.set_ylabel('Cantidad de viajes')
        ax.set_title('Viajes retrasados')
        ax.set_xticks(ind + bar_width / 2)
        ax.set_xticklabels(('lun', 'mar', 'mier', 'jue', 'vie', 'sab', 'dom'))
        ax.legend((delayed_flights_bar[0], total_flights_bar[0]), ('Viajes retrasados', 'Viajes totales'))
        plt.show()

    def show_flights_per_airport(dataset):
        new_dataset = []
        airports_limit = 45 #top limit of busiest Airports
        x = {}
        for i in range(len(dataset)):
            origin_airport_name = dataset[i].origin_airport_name
            if origin_airport_name not in x:
                x[origin_airport_name] = 0
            x[origin_airport_name] += 1
        print("Total flights number: {0}".format(len(dataset)))
        print("Total count of airports: {0}".format(len(x)))
        busiest_origin_airports = sorted(x, key=x.__getitem__, reverse=True)
        busiest_origin_airports = busiest_origin_airports[:airports_limit]
        flight_qty = 0
        print("bussiest_origin_airports: {0}".format(busiest_origin_airports))
        for key in busiest_origin_airports:
            flight_qty += x[key]
        print("Total flights in bussiest airports: {0}".format(flight_qty))
        print("% of flights in bussiest airports: {0}%".format( (flight_qty / len(dataset)) * 100.00 ))

    def pandas_data_visualization(dataset):
        attributes_array = []
        for i in range(len(dataset)):
            attributes_array.append(dataset[i].get_random_forest_property_array())
        df = pd.DataFrame(attributes_array)
        df.hist()
        plt.show()
