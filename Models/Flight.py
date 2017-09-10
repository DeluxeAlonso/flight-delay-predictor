import Utils
import Constants
from Models.Airport import Airport
from Models.Weather import Weather

class Flight:
    def __init__(self, year, quarter, month, day_of_month, day_of_week, date, airline_id, tail_number,flight_number,
                 origin_airport_id, origin_airport_name, destination_airport_id, destination_airport_name,
                 departure_time, real_departure_time, elapsed_time, distance):
        self.year = str(year)
        self.quarter = str(quarter)
        self.month = str(month)
        self.day_of_month = str(day_of_month)
        self.day_of_week = str(day_of_week)
        self.date = str(date)
        self.airline_id = str(airline_id)
        self.tail_number = str(tail_number)
        self.flight_number = str(flight_number)
        self.origin_airport = Airport(origin_airport_id, origin_airport_name)
        self.destination_airport = Airport(destination_airport_id, destination_airport_name)
        self.departure_time = self.get_time(departure_time)
        self.real_departure_time = real_departure_time
        self.elapsed_time = str(elapsed_time)
        self.distance = str(distance)
        self.cancelled = self.is_cancelled()
        if not self.cancelled:
            self.delayed = self.is_delayed()
        #Feature Engineering
        self.holiday = None
        self.days_to_holiday = None
        self.weather = None

    def get_numerical_property_array(self):
        properties = [float(self.elapsed_time), float(self.delayed)]
        if self.days_to_holiday is not None:
            properties.insert(len(properties) - 1, float(self.days_to_holiday))
        if self.weather is not None:
            properties[len(properties) - 1:len(properties) - 1] = self.weather.get_properties_array_without_wban_date()
        return properties

    def get_categorical_property_array(self):
        properties = [str(self.month), str(self.day_of_month),
                str(self.day_of_week), str(self.origin_airport.name),
                str(self.airline_id), str(self.destination_airport.name),
                str(self.get_departure_time_hour()), str(self.tail_number),
                float(self.delayed)]
        if self.holiday is not None:
            properties.insert(len(properties) - 1, str(self.holiday))
        return properties

    def get_random_forest_property_array(self):
        properties = [str(self.month), str(self.day_of_month),str(self.origin_airport.name),
                      str(self.destination_airport.name), str(self.day_of_week),
                      str(self.get_departure_time_hour()), str(self.flight_number),
                      str(self.tail_number), float(self.elapsed_time), float(self.delayed)]
        if self.holiday is not None:
            properties.insert(len(properties) - 1, float(self.holiday))
        if self.days_to_holiday is not None:
            properties.insert(len(properties) - 1, str(self.days_to_holiday))
        if self.weather is not None:
            properties[len(properties) - 1:len(properties) - 1] = self.weather.get_properties_array_without_wban_date()
        return properties

    def get_properties_array(self):
        properties = [self.year, self.quarter, self.month, self.day_of_month, self.day_of_week, self.date,
                self.airline_id, self.tail_number, self.flight_number, self.origin_airport.code,
                self.origin_airport.name, self.destination_airport.code, self.destination_airport.name, self.departure_time,
                self.real_departure_time, self.elapsed_time, self.distance, self.delayed]
        if self.holiday is not None:
            properties.insert(len(properties) - 1, float(self.holiday))
        if self.days_to_holiday is not None:
            properties.insert(len(properties) - 1, str(self.days_to_holiday))
        if self.origin_airport.wban is not None:
            properties.insert(len(properties) - 1, float(self.origin_airport.wban))
        if self.weather is not None:
            properties[len(properties) - 1:len(properties) - 1] = self.weather.get_properties_for_dataset()
        return properties

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
        return (real_departure_time - departure_time)/60.0 >= 15.00

    def is_cancelled(self):
        if self.real_departure_time == '' or self.real_departure_time == "nan" or self.real_departure_time == None:
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
            self.real_departure_time = self.get_time(str(int(real_departure_h)) + real_departure_m)
            self.delayed = True
            return True
        else:
            self.real_departure_time = self.get_time(self.real_departure_time)
            return False

    def get_time(self, departure_time):
        if len(departure_time) < 4:
            times = 4 - len(departure_time)
            prefix = ""
            for i in range(times):
                prefix = prefix + '0'
            departure_time = prefix + departure_time
            if departure_time == '0':
                print(departure_time)
        if departure_time == '0':
            print(departure_time)
        return departure_time

    def set_elapsed_time(self, elapsed_time):
        self.elapsed_time = elapsed_time

    def set_holiday(self, type=0):
        #0:Near day, 1:Near including day, 2: Only prior date, 3:only post date
        self.holiday = '0'
        if self.year == "2015":
            holidays = Constants.holidays_2015["national"]
        else:
            holidays = Constants.holidays_2016["national"]
        if type == 0:
            prior_date, post_date = Utils.Utils.get_near_dates(self.day_of_month, self.month, self.year)
            if prior_date in holidays or post_date in holidays:
                self.holiday = '1'
        elif type == 1:
            prior_date, current_date, post_date = Utils.Utils.get_near_dates(self.day_of_month, self.month,
                                                                             self.year, include_current = True)
            if prior_date in holidays or current_date in holidays or post_date in holidays:
                self.holiday = '1'
        elif type == 2:
            prior_date, post_date = Utils.Utils.get_near_dates(self.day_of_month, self.month, self.year)
            if prior_date in holidays:
                self.holiday = '1'
        elif type == 3:
            prior_date, post_date = Utils.Utils.get_near_dates(self.day_of_month, self.month, self.year)
            print(post_date)
            if post_date in holidays:
                self.holiday = '1'

    def set_days_to_holiday(self):
        evaluated_days = []
        formatted_date = Utils.Utils.get_date(self.day_of_month, self.month, self.year)
        if self.year == "2015":
            holidays = Constants.national_holidays_2015
        else:
            holidays = Constants.national_holidays_2016
        for i in range(len(holidays)):
            days_qty = abs(Utils.Utils.days_difference_between_dates(formatted_date, holidays[i]))
            evaluated_days.append(days_qty)
        self.days_to_holiday = min(evaluated_days)

