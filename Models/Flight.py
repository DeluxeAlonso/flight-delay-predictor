class Flight:
    def __init__(self, quarter, month, day_of_month, day_of_week, airline_id, tail_number,flight_number,
                 origin_airport_id, origin_airport_name, destination_airport_id, destination_airport_name,
                 departure_time, real_departure_time, elapsed_time, distance):
        self.quarter = quarter
        self.month = month
        self.day_of_month = day_of_month
        self.day_of_week = day_of_week
        self.airline_id = airline_id
        self.tail_number = tail_number
        self.flight_number = flight_number
        self.origin_airport_id = origin_airport_id
        self.origin_airport_name = origin_airport_name
        self.destination_airport_id = destination_airport_id
        self.destination_airport_name = destination_airport_name
        self.departure_time = departure_time
        self.real_departure_time = real_departure_time
        self.elapsed_time = elapsed_time
        self.distance = distance
        self.day_of_month_quarter = self.get_day_of_month_quarter()
        self.departure_time_quarter = self.get_departure_time_quarter()
        self.delayed = self.is_delayed()

    def get_numerical_property_array(self):
        return [float(self.departure_time), float(self.delayed)]

    def get_categorical_property_array(self):
        return [str(self.month), str(self.day_of_month),
                str(self.day_of_week), str(self.origin_airport_name),
                str(self.airline_id),
                float(self.delayed)]

    def get_departure_time_quarter(self):
        float_departure_time = float(self.departure_time)
        if 0.00 <= float_departure_time < 600.00:
            return 1
        elif 600.00 <= float_departure_time < 1200.00:
            return 2
        elif 1200.00 <= float_departure_time < 1800.00:
            return 3
        else:
            return 4

    def get_day_of_month_quarter(self):
        float_day_of_month = float(self.day_of_month)
        if 1.00 <= float_day_of_month < 8.00:
            return 1
        elif 8.00 <= float_day_of_month < 15.00:
            return 2
        elif 15.00 <= float_day_of_month < 22.00:
            return 3
        elif 22.00 <= float_day_of_month < 29.00:
            return 4
        else:
            return 5

    def is_delayed(self):
        return float(self.real_departure_time) - float(self.departure_time) > 15
