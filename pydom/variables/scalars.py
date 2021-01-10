from pydom.operations.variation import Delta
from types import new_class
from pydom.variables.variables import Expr, ScalarExpr
from pydom.variables import Variable

class Scalar(Variable):
    def __init__(self, s=None, value=None, assumptions=None):
        super(Scalar, self).__init__(s)
        self.size = (1,)
        self.value = value
        self.assumptions = assumptions
        self.__type__ = type(ScalarExpr())

    def __str__(self):
        return super(Scalar, self).__str__()

    def delta(self):
        name = 'delta{'+self.name+'}'
        delta_cls = Delta(Scalar(name, value=self.value))
        return delta_cls