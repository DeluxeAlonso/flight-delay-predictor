
#Files

monthly_training_folder = "Datasets/NewYork/Training/Monthly/"
monthly_testing_folder = "Datasets/NewYork/Testing/Monthly/"
month_labels = ["january", "february", "march", "april", "may",
                "june", "july", "august", "september", "october",
                "november", "december"]
output_training_merge_filename = "Datasets/NewYork/Training/merged_training.csv"
output_testing_merge_filename = "Datasets/NewYork/Testing/merged_testing.csv"

#Weather Daily Files

weather_daily_training_folder = "Datasets/NewYork/Weather/2015/Daily/Original/"
weather_daily_testing_folder = "Datasets/NewYork/Weather/2016/Daily/Original/"
weather_daily_training_labels = ["201501daily", "201502daily", "201503daily", "201504daily",
                                 "201505daily", "201506daily", "201507daily", "201508daily",
                                 "201509daily", "201510daily", "201511daily", "201512daily"]
weather_daily_testing_labels = ["201601daily", "201602daily", "201603daily", "201604daily",
                                 "201605daily", "201606daily", "201607daily", "201608daily",
                                 "201609daily", "201610daily", "201611daily", "201612daily"]
output_training_weather_merged_filename = "Datasets/NewYork/Weather/2015/Daily/merged_training.csv"
output_testing_weather_merged_filename = "Datasets/NewYork/Weather/2016/Daily/merged_testing.csv"
output_training_weather_filename = "Datasets/NewYork/Weather/2015/Daily/TrainingWeatherDataset.csv"
output_testing_weather_filename = "Datasets/NewYork/Weather/2016/Daily/TestingWeatherDataset.csv"

#Weather Hourly Files

weather_hourly_training_folder = "Datasets/NewYork/Weather/2015/Hourly/Original/"
weather_hourly_testing_folder = "Datasets/NewYork/Weather/2016/Hourly/Original/"
weather_hourly_training_labels = ["201501hourly", "201502hourly", "201503hourly", "201504hourly",
                                 "201505hourly", "201506hourly", "201507hourly", "201508hourly",
                                 "201509hourly", "201510hourly", "201511hourly", "201512hourly"]
weather_hourly_testing_labels = ["201601hourly", "201602hourly", "201603hourly", "201604hourly",
                                 "201605hourly", "201606hourly", "201607hourly", "201608hourly",
                                 "201609hourly", "201610hourly", "201611hourly", "201612hourly"]
output_training_weather_hourly_merged_filename = "Datasets/NewYork/Weather/2015/Hourly/merged_training.csv"
output_testing_weather_hourly_merged_filename = "Datasets/NewYork/Weather/2016/Hourly/merged_testing.csv"
output_training_weather_hourly_filename = "Datasets/NewYork/Weather/2015/Hourly/TrainingWeatherDataset.csv"
output_testing_weather_hourly_filename = "Datasets/NewYork/Weather/2016/Hourly/TestingWeatherDataset.csv"

#Holiday Feature

holidays_2015 = {"national": ["02/01/2015", "12/02/2015", "16/02/2015", "10/05/2015",
                              "21/06/2015", "11/11/2015", "25/12/2015", "30/12/2015"]}
holidays_2016 = {"national": ["02/01/2016", "12/02/2016", "15/02/2016", "08/05/2016",
                              "19/06/2016", "11/11/2016", "25/12/2016", "30/12/2016"]}

#DaysToHoliday Feature

national_holidays_2015 = ["01/01/2015", "19/01/2015", "25/05/2015", "03/07/2015", "07/09/2015", "26/11/2015", "25/12/2015", "31/12/2015"]
national_holidays_2016 = ["01/01/2016", "18/01/2016", "30/05/2016", "04/07/2016", "05/09/2016", "11/11/2016","24/11/2016", "25/12/2016", "31/12/2016"]

#Dataframe Header

df_header = ['MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'ORIGIN_AIRPORT', 'DEST_AIRPORT', 'DEPARTURE_TIME', 'FL_NUMBER', 'TAIL_NUMBER', 'ELAPSED_TIME', 'DAYS_TO_HOLIDAY', 'TEMPERATURE', 'SKY_CONDITION', 'WIND_SPEED', 'PRESSURE', 'HUMIDITY', 'ALTIMETER', 'RAIN', 'SNOW', 'FOG', 'MIST', 'FREEZING', 'DELAYED']