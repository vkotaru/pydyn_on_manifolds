import numpy as np
from pydyn.data_types.expr import Expression, Expr
from pydyn.operations.addition import Add, VAdd, MAdd
from pydyn.operations.multiplication import SVMul, VVMul, MVMul
from pydyn.operations.geometry import Delta, Dot, Cross
from pydyn.utils.errors import ExpressionMismatchError, UndefinedCaseError


class Vector(Expr):
    def __init__(self, s=None, size=3, value=None, attr=None):
        super().__init__()
        self.name = s
        self.size = (size,)
        if value is None:
            self.value = np.empty(size, dtype='object')
        else:
            self.value = value
            self.size = self.value.shape
        self.type = Expression.VECTOR
        self.attr = attr  # Constant, Zero, Ones

    def __str__(self):
        return self.name

    def __add__(self, other):
        if other.type == Expression.VECTOR:
            return VAdd(self, other)
        else:
            raise ExpressionMismatchError

    def __mul__(self, other):
        if other.type == Expression.SCALAR:
            return SVMul(self, other)
        elif other.type == Expression.VECTOR:
            return VVMul(self, other)
        elif other.type == Expression.MATRIX:
            return MVMul(self, other)
        else:
            return UndefinedCaseError

    def delta(self):
        if self.isOnes or self.isZero or self.isConstant:
            return Vector('0', attr=['Constant', 'Zero'])
        else:
            name = 'delta{' + self.name + '}'
            delta_cls = Delta(Vector(name, value=self.value))
            return delta_cls

    def dot(self, other):
        return Dot(self, other)

    def cross(self, other):
        return Cross(self, other)

    def diff(self):
        if self.isConstant:
            return Vector(s='0', size=self.size, attr=['Constant', 'Zero'])
        else:
            return Vector(s='dot_' + self.name, size=self.size)


def getVectors(input):
    if isinstance(input, list):
        vars = input
    elif isinstance(input, str):
        vars = input.split()
    else:
        return None
    s = []
    for v in vars:
        s.append(Vector(v))
    return tuple(s)
