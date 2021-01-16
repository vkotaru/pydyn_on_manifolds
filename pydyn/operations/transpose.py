import pydyn.data_types

class Transpose(object):
    def __init__(self, expr):
        self.expr = expr
        self.type = 'VectorExpr'

    # def delta(self):
    #     return Transpose(Delta(self.expr))