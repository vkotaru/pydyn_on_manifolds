from pydom.variables.variables import VectorExpr
from pydom.variables import Variable, Scalar
import numpy as np

class Vector(Variable):
    """
    Symbolic Vector class
    """
    def __init__(self, s=None, size=3):
        super().__init__(s)
        self.size = (size,)
        self.value = np.empty(size, dtype='object')
        self.__type__ == type(VectorExpr())

    def __str__(self):
        return super().__str__()
