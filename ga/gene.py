"""
	optimize.ga.gene
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Implements class for manage gene.
	:copyright: Hwang.S.J.
	:license: MIT LICENSE 1.0 .
"""

from .dtype import DType


class Gene(DType):
    def __init__(self, dtype, value_range, isNormal=False):
        super(Gene, self).__init__(dtype, value_range, isNormal)

    def mutation(self):
        self.get_value()
