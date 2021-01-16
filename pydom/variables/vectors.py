from pydom.operations.variation import Delta
from pydom.variables.variables import VectorExpr, Variable
import numpy as np

class Vector(Variable):
    """
    Symbolic Vector class
    """
    def __init__(self, s=None, size=3, value=None, attr=None):
        super().__init__(s)
        self.size = (size,)
        if value is None:
            self.value = np.empty(size, dtype='object')
        else: 
            self.value = value
        self.__type__ == type(VectorExpr())

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
            return Vector('0', attr=['Constant', 'Zero'])
        else:
            name = 'delta{'+self.name+'}'
            delta_cls = Delta(Vector(name, value=self.value))
            return delta_cls

