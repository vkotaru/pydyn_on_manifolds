from pydom.variables.variables import MatrixExpr, Variable
from pydom.operations.variation import Delta
import numpy as np


class Matrix(Variable):
    def __init__(self, s=None, size=(3,3), value=None, attr=None):
        super().__init__(s=s)
        self.size = size
        if value is None:
            self.value = np.empty(size, dtype='object')
        else:
            self.value = value
        self.__type__ = type(MatrixExpr())
        
        self.attr = attr # Constant, Zero, Ones
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
        return super().__str__()

    def delta(self):
        if self.isOnes or self.isZero or self.isConstant:
            return Matrix('0', attr=['Constant', 'Zero'])
        else:
            name = 'delta{'+self.name+'}'
            delta_cls = Delta(Matrix(name, value=self.value))
            return delta_cls



    
