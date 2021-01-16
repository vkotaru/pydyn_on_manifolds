from pydom.variables.variables import Variable
from pydom.operations.variation import Delta
from pydom.variables.variables import Expr

class Transpose(Expr):
    def __init__(self, expr=Variable()):
        super().__init__()
        self.expr = expr
        self.__type__ = expr.__type__

    def delta(self):
        return Transpose(Delta(self.expr))