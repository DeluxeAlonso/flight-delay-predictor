from Solver import Solver
from Models.Flight import Flight

class Main:
    def load_data(self):
        filename = 'Datasets/training.csv'
        dataset = Solver.load_csv(filename)
        separated_dataset = Solver.separate_by_class(dataset)
        summary = Solver.summarize(dataset)
        separated_sumary = Solver.summarize_by_class(separated_dataset)
        print('Loaded data file {0} with {1} rows'.format(filename, len(dataset)))
        print('Separated instances: {0}'.format(separated_dataset))
        print('First row data date: {0}'.format(dataset[0].get_property_array()))
        print('Attribute summaries: {0}'.format(summary))
        print('Attribute summaries by classes: {0}'.format(separated_sumary))

Main().load_data()