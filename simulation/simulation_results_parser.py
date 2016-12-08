#!/usr/bin/python3
import print_data_model

# Typical Results looks like:
example = '''
'''

# Parse output of simulation run
class SimulationMetrics(print_data_model.MetricContainer):
    def __init__(self, datastring):
        # Initialize empty lists for metrics
        metric_list = []
        title_list  = []
        data_list   = []
        print_data_model.MetricContainer.__init__(self, metric_list, title_list, data_list)

# Use argparsing from base module
if __name__ == '__main__':
    print_data_model.main(SimulationMetrics, example)
