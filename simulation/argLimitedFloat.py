class Range(object):
    def __init__(self, start=0, end=float('inf')):
        self.start = start
        self.end = end
    def __eq__(self, val):
        return self.start <= val <= self.end
    def __repr__(self):
        return 'interval [{0}, {1}]'.format(self.start, self.end)
