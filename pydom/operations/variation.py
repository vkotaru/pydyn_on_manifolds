from pydom.variables.variables import Expr

class Delta(Expr):
    def __init__(self, expr=None):
        self.expr = expr 
        self.__type__ = expr.__type__

    def __str__(self):
        return self.expr.__str__()
