"""
	optimize.ga.dtype
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements tools for manage gene's data in chromosome.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from numpy.random import normal
from random import uniform, choice


class DType(object):
    def __init__(self, dtype, value_range, isNormal=False):
        self.value = None
        self.dtype = dtype
        self.value_range = value_range
        self.isNormal = isNormal

        if self.dtype not in ['int', 'float', 'choice']:
            raise ValueError

        self.get_value()

    def get_value(self):
        if self.dtype == 'choice':
            self.value = choice(self.value_range)
            return

        if len(self.value_range) != 2:
            raise TypeError

        self.value_range.sort()
        tmp_value = normal(sum(self.value_range) / 2, 1) if self.isNormal else uniform(self.value_range[0],
                                                                                       self.value_range[1])

        if tmp_value < self.value_range[0]:
            self.value = self.value_range[0]
        elif tmp_value > self.value_range[1]:
            self.value = self.value_range[1]

        else:
            if self.dtype == 'int':
                self.value = round(tmp_value)
            else:
                self.value = tmp_value

        if self.dtype == 'int':
            self.value = int(self.value)
        elif self.dtype == 'float':
            self.value = float(self.value)
