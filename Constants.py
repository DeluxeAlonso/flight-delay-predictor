
#Files

monthly_training_folder = "Datasets/NewYork/Training/Monthly/"
monthly_testing_folder = "Datasets/NewYork/Testing/Monthly/"
month_labels = ["january", "february", "march", "april", "may",
                "june", "july", "august", "september", "october",
                "november", "december"]
output_training_merge_filename = "Datasets/NewYork/Training/merged_training.csv"
output_testing_merge_filename = "Datasets/NewYork/Testing/merged_testing.csv"

#Holiday Feature

holidays_2015 = {"national": ["02/01/2015", "12/02/2015", "16/02/2015", "10/05/2015",
                              "21/06/2015", "11/11/2015", "25/12/2015", "30/12/2015"]}
holidays_2016 = {"national": ["02/01/2016", "12/02/2016", "15/02/2016", "08/05/2016",
                              "19/06/2016", "11/11/2016", "25/12/2016", "30/12/2016"]}

#DaysToHoliday Feature

national_holidays_2015 = ["01/01/2015", "19/01/2015", "25/05/2015", "03/07/2015", "07/09/2015", "26/11/2015", "25/12/2015", "31/12/2015"]
national_holidays_2016 = ["01/01/2016", "18/01/2016", "30/05/2016", "04/07/2016", "05/09/2016", "11/11/2016","24/11/2016", "25/12/2016", "31/12/2016"]