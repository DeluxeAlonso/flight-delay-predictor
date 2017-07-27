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
        self.cancelled = self.is_cancelled()
        self.delayed = self.is_delayed()

    def get_numerical_property_array(self):
        return [ float(self.distance), float(self.elapsed_time), float(self.delayed)]

    def get_categorical_property_array(self):
        return [str(self.month), str(self.day_of_month),
                str(self.day_of_week), str(self.origin_airport_name),
                str(self.airline_id), str(self.destination_airport_name),
                str(self.get_departure_time_hour()), str(self.tail_number),
                float(self.delayed)]

    def get_random_forest_property_array(self):
        return [str(self.month), str(self.origin_airport_name), str(self.destination_airport_name),
                str(self.day_of_week),str(self.get_departure_time_hour()), float(self.distance),
                float(self.elapsed_time), float(self.delayed)]

    def get_all_property_array(self):
        return [self.quarter, self.month, self.day_of_month, self.day_of_week,
                self.airline_id, self.tail_number, self.flight_number, self.origin_airport_id,
                self.origin_airport_name, self.destination_airport_id, self.destination_airport_name, self.departure_time,
                self.real_departure_time, self.elapsed_time, self.distance]

    def get_departure_time_hour(self):
        if len(self.departure_time) == 3:
            return self.departure_time[0]
        else:
            return self.departure_time[0] + self.departure_time[1]

    def get_time_hour_minutes(self, time):
        if len(time) == 3:
            hour = time[0]
            minutes = time[1] + time[2]
            return hour, minutes
        else:
            hour = time[0] + time[1]
            minutes = time[2] + time[3]
            return hour, minutes

    def is_delayed(self):
        departure_h, departure_m = self.get_time_hour_minutes(self.departure_time)
        real_departure_h, real_departure_m = self.get_time_hour_minutes(self.real_departure_time)
        departure_time = float(departure_h) * 3600.00 + float(departure_m) * 60.00
        real_departure_time = float(real_departure_h) * 3600.00 + float(real_departure_m) * 60.00
        return (real_departure_time - departure_time)/60.0 > 15.00

    def is_cancelled(self):
        if self.real_departure_time == '':
            if len(self.departure_time) < 3:
                self.departure_time = self.departure_time + '00'
            departure_h, departure_m = self.get_time_hour_minutes(self.departure_time)
            if 60.0 - float(departure_m) > 15.0:
                real_departure_m = float(departure_m) + 15.0
                real_departure_h = float(departure_h)
            else:
                real_departure_h = float(departure_h) + 1.0
                real_departure_m = 15.0 - (60.0 - float(departure_m))
            if real_departure_m < 10.0:
                real_departure_m = "0" + str(int(real_departure_m))
            else:
                real_departure_m = str(int(real_departure_m))
            self.real_departure_time = str(int(real_departure_h)) + real_departure_m
            return True
        else:
            return False