class Flight:
    def __init__(self, month, day_of_month, day_of_week, date, departure_time, real_departure_time):
        self.month = month
        self.day_of_month = day_of_month
        self.day_of_week = day_of_week
        self.date = date
        self.departure_time = departure_time
        self.real_departure_time = real_departure_time
        self.delayed = self.is_delayed()

    def get_property_array(self):
        return [float(self.month), float(self.day_of_month),
                float(self.day_of_week), float(self.departure_time),
                float(self.real_departure_time), float(self.delayed)]

    def is_delayed(self):
        return float(self.real_departure_time) - float(self.departure_time) > 15