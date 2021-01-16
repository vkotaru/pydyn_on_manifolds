from pydyn.operations.addition import MAdd
import numpy as np


class Matrix(object):
    def __init__(self, s=None, size=(3, 3), value=None, attr=None):
        self.name = s
        self.size = size
        if value is None:
            self.value = np.empty(size, dtype='object')
        else:
            self.value = value
        self.type = 'MatrixExpr'

        self.attr = attr  # Constant, Zero, Ones
        if attr is not None:
            if 'Zero' in attr:
                self.isZero = True
                self.isConstant = True
            else:
                self.isZero = False
            if 'Ones' in attr:
                self.isOnes = True
                self.isConstant = True
            else:
                self.isOnes = False
            if 'Constant' in attr:
                self.isConstant = True

    def __str__(self):
        return self.name

    def __add__(self, other):
        if other.type == 'MatrixExpr':
            return MAdd(self, other)
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError  # def delta(self):  #     if self.isOnes or self.isZero or self.isConstant:  #         return Matrix('0', attr=['Constant', 'Zero'])  #     else:  #         name = 'delta{'+self.name+'}'  #         delta_cls = Delta(Matrix(name, value=self.value))  #         return delta_cls  #  #  #  #
