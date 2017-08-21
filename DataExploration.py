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

    def generate_flight_bar_tuples(x, y, max_range):
        delayed_flights = ()
        total_flights = ()
        for i in range(max_range):
            delayed_flights += (x[i],)
            total_flights += (y[i],)
        return delayed_flights, total_flights

    def show_delays_per_month(dataset, normed=False):
        x = [0] * n_months
        y = [0] * n_months
        for i in range(len(dataset)):
            property_array = dataset[i].get_categorical_property_array()
            index = int(property_array[0]) - 1
            y[index] += 1
            if property_array[-1] == 1.0:
                x[index] += 1
        if normed:
            for i in range(len(y)):
                x[i] = x[i] / y[i]
                y[i] = 1.0
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

    def show_delays_per_day_of_week(dataset, normed=False):
        x = [0] * n_days_per_week
        y = [0] * n_days_per_week
        for i in range(len(dataset)):
            property_array = dataset[i].get_categorical_property_array()
            index = int(property_array[2]) - 1
            y[index] += 1
            if property_array[-1] == 1.0:
                x[index] += 1
        if normed:
            for i in range(len(y)):
                x[i] = x[i] / y[i]
                y[i] = 1.0
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

    def show_delays_per_holiday(dataset, normed=False):
        x = [0]
        y = [0]
        for i in range(len(dataset)):
            flight = dataset[i]
            property_array = flight.get_categorical_property_array()
            if flight.holiday == '1':
                y[0] += 1
                if property_array[-1] == 1.0:
                    x[0] += 1
        if normed:
            x[0] = x[0] / y[0]
            y[0] = 1
        print("total {0}".format(y[0]))
        print("retrasados {0}".format(x[0]))
        ind = np.arange(1)
        fig, ax = plt.subplots()
        delayed_flights_tuple, total_flights_tuple = DataExploration.generate_flight_bar_tuples(x, y, 1)
        delayed_flights_bar = ax.bar(ind, delayed_flights_tuple, bar_width, color='r')
        total_flights_bar = ax.bar(ind + bar_width, total_flights_tuple, bar_width, color='y')
        ax.set_ylabel('Cantidad de viajes')
        ax.set_title('Viajes retrasados')
        ax.set_xticks(ind + bar_width / 2)
        ax.set_xticklabels(('Holiday', 'Holiday'))
        ax.legend((delayed_flights_bar[0], total_flights_bar[0]), ('Viajes retrasados', 'Viajes totales'))
        plt.show()

    def show_delays_per_dep_hour(dataset, normed=False):
        x = [0] * 24
        y = [0] * 24
        for i in range(len(dataset)):
            flight = dataset[i]
            property_array = flight.get_categorical_property_array()
            index = int(flight.get_departure_time_hour())
            y[index] += 1
            if property_array[-1] == 1.0:
                x[index] += 1
        if normed:
            for i in range(len(y)):
                x[i] = x[i] / y[i]
                y[i] = 1.0
        ind = np.arange(24)
        fig, ax = plt.subplots()
        delayed_flights_tuple, total_flights_tuple = DataExploration.generate_flight_bar_tuples(x, y, 24)
        delayed_flights_bar = ax.bar(ind, delayed_flights_tuple, bar_width, color='r')
        total_flights_bar = ax.bar(ind + bar_width, total_flights_tuple, bar_width, color='y')
        ax.set_ylabel('Cantidad de viajes')
        ax.set_title('Hora de despegue')
        ax.set_xticks(ind + bar_width / 2)
        ax.set_xticklabels(('00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
                            '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'))
        ax.legend((delayed_flights_bar[0], total_flights_bar[0]), ('Viajes retrasados', 'Viajes totales'))
        plt.show()

    def show_flights_per_airport(dataset):
        new_dataset = []
        airports_limit = 10 #top limit of busiest Airports
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

    def show_delay_reason_pie_chart(filename):
        dataset = pd.read_csv(filename)
        labels = 'Carrier', 'Weather', 'NAS', 'Security', "Aircraft"
        chart_array = [0, 0, 0, 0, 0]
        matrix = dataset.as_matrix()
        for i in range(len(matrix)):
            if matrix[i][24] >= 15:
                chart_array[0] += 1
            elif matrix[i][25] >= 15:
                chart_array[1] += 1
            elif matrix[i][26] >= 15:
                chart_array[2] += 1
            elif matrix[i][27] >= 15:
                chart_array[3] += 1
            elif matrix[i][28] >= 15:
                chart_array[4] += 1
        fig1, ax1 = plt.subplots()
        ax1.pie(chart_array, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')
        plt.show()

    def show_time_distance_correlation(dataset):
        elapsed_times = []
        distances = []
        for i in range(len(dataset)):
            flight = dataset[i]
            elapsed_times.append(flight.elapsed_time)
            distances.append(flight.distance)
        area = np.pi
        plt.ylabel('Distancia')
        plt.xlabel('Tiempo estimado')
        plt.scatter(np.array(elapsed_times), np.array(distances), s=area, alpha=0.5)
        plt.show()

    def pandas_data_visualization(dataset):
        attributes_array = []
        for i in range(len(dataset)):
            attributes_array.append(dataset[i].get_random_forest_property_array())
        df = pd.DataFrame(attributes_array)
        df.hist()
        plt.show()
