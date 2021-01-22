from pydyn.data_types.expr import Expr, Expression
from pydyn.operations.nodes import UnaryNode
from pydyn.utils.errors import UndefinedCaseError, ExpressionMismatchError


class Transpose(Expr, UnaryNode):
    def __init__(self, expr=None):
        super().__init__()
        if expr is not None:
            self.expr = expr
            self.type = expr.type

    def __str__(self):
        return '('+self.expr.__str__() + ')\''

    def __add__(self, other):
        from pydyn.operations.addition import Add, VAdd, MAdd
        if self.type == Expression.SCALAR and other.type == Expression.SCALAR:
            return Add(self, other)
        elif self.type == Expression.VECTOR and other.type == Expression.VECTOR:
            return VAdd(self, other)
        elif self.type == Expression.MATRIX and other.type == Expression.MATRIX:
            return MAdd(self, other)
        else:
            raise ExpressionMismatchError('mul', 'Transpose(' + self.type + ')', other.type)

    def __mul__(self, other):
        if other.type == Expression.SCALAR:
            from pydyn.operations.multiplication import SVMul
            return Transpose(SVMul(self, other))
        elif other.type == Expression.VECTOR:
            from pydyn.operations.multiplication import VVMul
            return VVMul(self, other)
        elif other.type == Expression.MATRIX:
            from pydyn.operations.multiplication import MVMul
            return MVMul(self, other)
        else:
            raise ExpressionMismatchError('mul', 'Transpose(' + self.type + ')', other.type)

    def delta(self):
        return Transpose(self.expr.delta())