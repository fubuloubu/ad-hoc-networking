#!/usr/bin/python3
import print_data_model

# Typical Results looks like:
example = '''
Statistics:
Total Messages: 64
Succesfully Received Messages: 6
Success Rate: 9.38%
Number of Retransmissions: 188
Average Latency: 0.00 [steps]

Statistics:
Total Messages: 52
Succesfully Received Messages: 4
Success Rate: 7.69%
Number of Retransmissions: 208
Average Latency: 0.00 [steps]

Statistics:
Total Messages: 53
Succesfully Received Messages: 4
Success Rate: 7.55%
Number of Retransmissions: 188
Average Latency: 0.00 [steps]
'''
# NOTE: Multiple Simulations possible...

def sanitize(resultsStr):
    resultsStr = resultsStr.lstrip().rstrip()
    oldLen = 0
    while (len(resultsStr) != oldLen):
        resultsStr = resultsStr.replace('\n\n','\n')
        oldLen = len(resultsStr)
    return resultsStr

import re
def extractMetrics(metricString):
    metric = {}
    metricString = metricString.split(': ')
    metric["title"] = metricString[0]
    metric["mname"] = metricString[0].lower().replace(' ','-')
    match = re.search(r'([0-9.]+) *(.*)', metricString[1])
    if match:
        (data, units) = match.group(1,2)
        metric["value"] = data
        metric["units"] = 'none' if units == '' else \
            units.lstrip().replace('[','').replace(']','')
    else:
        raise ValueError("'{}' does not parse with regex".format(metricString[1]))
    return metric

# Parse output of simulation run
class SimulationMetrics(print_data_model.MetricContainer):
    def __init__(self, datastring):
        # Clean data string and split by simulation run
        simStats = sanitize(datastring).split('Statistics:\n')
        # Remove empty entries and split by line
        simStats = filter(None, simStats)
        simStats = map(lambda s: s.rstrip().split('\n'), simStats)
        # Parse each raw metric line into a metric object
        # NOTE: Using list here because below we need to use it again
        simStats = list(map(lambda s: list(map(lambda ms: extractMetrics(ms), s)), simStats))
        
        # Make sure metric names in each simulation line up
        # e.g. there are N duplicates of every metric in list
        metricNames = map(lambda s: [ m["mname"] for m in s], simStats)
        def checkEqual(iterator):
            iterator = iter(iterator)
            try:
                first = next(iterator)
            except StopIteration:
                return True
            return all(first == rest for rest in iterator)
        # Raise error if fault is found
        if not checkEqual(metricNames):
            raise ValueError("Simulations do not have matching metrics")

        # Create lists by mapping each simulation metric 
        # to unique metric name using position in list
        metricNames  = [ m["mname"] for m in simStats[0] ]
        metricTitles = [ m["title"] for m in simStats[0] ]
        metricUnits  = [ m["units"] for m in simStats[0] ]
        
        metric_list = []
        title_list  = []
        for i in range(len(simStats)):
            for j in range(len(metricNames)):
                metric_list.append("{1}-{0:02d}".format(i+1, metricNames[j]))
                title_list.append("Simulation {0} {1} [{2}]".
                        format(i+1, metricTitles[j], metricUnits[j]))
        from ast import literal_eval
        # Get data list by extracting value from metrics and flattening that list
        # NOTE: Using list here because below we need to use it again
        metricData = list(map(lambda s: [ m["value"] for m in s], simStats))
        data_list  = [literal_eval(item) for sublist in metricData for item in sublist]
        
        # Add average metrics
        avgMetricData = map(lambda l: sum(map(literal_eval, l)), metricData)
        avgMetricData = map(lambda avg: avg/float(len(simStats)), avgMetricData)
        # NOTE: Using list here because below we need use subscripts
        avgMetricData = list(avgMetricData)
        for i in range(len(simStats)):
            metric_list.append("avg-{0}".format(metricNames[i]))
            title_list.append("Average Simulation {0} [{1}]".
                    format(metricTitles[i], metricUnits[i]))
            data_list.append(avgMetricData[i])
        
        # Initialize container for all metrics we discovered
        print_data_model.MetricContainer.__init__(self, metric_list, title_list, data_list)

# Use argparsing from base module
if __name__ == '__main__':
    print_data_model.main(SimulationMetrics, example)
