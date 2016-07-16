import numpy


def median(lst):
    return numpy.median(numpy.array(lst))


def mean(lst):
    return float(sum(lst))/len(lst) if len(lst) > 0 else float('nan')