"""
Base classes for variables
"""


class Variable(object):
    def __init__(self, s=''):
        self.name = s
        self.size = ()
        self.__type__ = None

    def __str__(self):
        return self.name


class Expr(Variable):
    def __init__(self):
        self.variables = []

class ScalarExpr(Expr):
    def __init__(self):
        pass

class VectorExpr(Expr):
    def __init__(self):
        pass

class MatrixExpr(Expr):
    def __init__(self):
        pass
