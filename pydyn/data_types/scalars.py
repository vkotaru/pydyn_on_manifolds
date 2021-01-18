from pydyn.data_types.expr import Expr, Expression
from pydyn.operations.addition import Add, VAdd, MAdd
from pydyn.operations.geometry import Delta
from pydyn.operations.multiplication import Mul, SVMul, SMMul
from pydyn.utils.errors import ExpressionMismatchError, UndefinedCaseError


class Scalar(Expr):
    def __init__(self, s=None, value=None, attr=None):
        super().__init__()
        self.name = s
        self.size = (1,)
        self.value = value
        self.type = Expression.SCALAR
        self.attr = attr

    def __str__(self):
        return self.name

    def __add__(self, other):
        if other.type == Expression.SCALAR:
            return Add(self, other)
        else:
            raise ExpressionMismatchError('Add', self.type, other.type)

    def __mul__(self, other):
        if other.type == Expression.SCALAR:
            return Mul(self, other)
        elif other.type == Expression.VECTOR:
            return SVMul(other, self)
        elif other.type == Expression.MATRIX:
            return SMMul(other, self)
        else:
            raise UndefinedCaseError

    def delta(self):
        if self.isConstant:
            return Scalar('0', value=0)
        else:
            return Delta(self)


def getScalars(input, attr=None):
    if isinstance(input, list):
        vars = input
    elif isinstance(input, str):
        vars = input.split()
    else:
        return None
    s = []
    for v in vars:
        s.append(Scalar(v, attr=attr))
    return tuple(s)
