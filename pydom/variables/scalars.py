from pydom.operations.variation import Delta
from pydom.variables.variables import Expr, ScalarExpr, Variable

class Scalar(Variable):
    def __init__(self, s=None, value=None, attr=None):
        super(Scalar, self).__init__(s)
        self.size = (1,)
        self.value = value
        self.__type__ = type(ScalarExpr())

        self.attr = attr
        if (self.attr == 'Constant'):
            self.isConstant = True
        else:
            self.isConstant = False

    def __str__(self):
        return super(Scalar, self).__str__()

    def delta(self):
        if self.isConstant:
            return Scalar('0', value=0)
        else:
            name = 'delta{'+self.name+'}'
            delta_cls = Delta(Scalar(name, value=self.value))
            return delta_cls