class Flight:
    def __init__(self, month, day_of_month, day_of_week, date, origin_airport_id, origin_ariport_name, departure_time, real_departure_time):
        self.month = month
        self.day_of_month = day_of_month
        self.day_of_week = day_of_week
        self.date = date
        self.origin_airport_id = origin_airport_id
        self.origin_airport_name = origin_ariport_name
        self.departure_time = departure_time
        self.real_departure_time = real_departure_time
        self.quarter = self.get_month_quarter()
        self.day_of_month_quarter = self.get_day_of_month_quarter()
        self.depature_time_quarter = self.get_departure_time_quarter()
        self.delayed = self.is_delayed()

    def get_property_array(self):
        return [float(self.month), float(self.day_of_month_quarter),
                float(self.day_of_week), float(self.depature_time_quarter),
                float(self.delayed)]

    def get_month_quarter(self):
        float_month = float(self.month)
        if 1.00 <= float_month < 5.00:
            return 1
        elif 5.00 <= float_month < 9.00:
            return 2
        elif 9.00 <= float_month < 12.00:
            return 3

    def get_departure_time_quarter(self):
        float_departure_time = float(self.departure_time)
        if 0.00 <= float_departure_time < 6.00:
            return 1
        elif 6.00 <= float_departure_time < 12.00:
            return 2
        elif 12.00 <= float_departure_time < 18.00:
            return 3
        else:
            return 4

    def get_day_of_month_quarter(self):
        float_day_of_month = float(self.day_of_month)
        if 1.00 <= float_day_of_month < 7.00:
            return 1
        elif 7.00 <= float_day_of_month < 13.00:
            return 2
        elif 13.00 <= float_day_of_month < 19.00:
            return 3
        elif 19.00 <= float_day_of_month < 25.00:
            return 4
        else:
            return 5

    def is_delayed(self):
        return float(self.real_departure_time) - float(self.departure_time) > 15
