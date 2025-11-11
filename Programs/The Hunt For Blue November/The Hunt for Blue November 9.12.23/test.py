from time import sleep
import math as m
import numpy as np

def test(bar):
    bar = bar*bar
    return bar

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("test(4)", setup="from __main__ import test"))