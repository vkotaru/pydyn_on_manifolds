import numpy as np
from pydyn.data_types.expr import Expression, Expr
from pydyn.operations.transpose import Transpose
from pydyn.utils.errors import UndefinedCaseError, ExpressionMismatchError


class MatrixExpr(Expr):
    def __init__(self):
        super().__init__()
        self.type = Expression.MATRIX

    def __str__(self):
        raise NotImplementedError

    def __add__(self, other):
        from pydyn.operations.addition import MAdd
        if other.type == Expression.MATRIX:
            return MAdd(self, other)
        else:
            raise ExpressionMismatchError

    def __mul__(self, other):
        from pydyn.operations.multiplication import SMMul, MVMul, MMMul
        if other.type == Expression.SCALAR:
            return SMMul(self, other)
        elif other.type == Expression.VECTOR:
            if type(other) == type(Transpose(None)):
                raise ExpressionMismatchError
            else:
                return MVMul(self, other)
        elif other.type == Expression.MATRIX:
            return MMMul(self, other)
        else:
            raise UndefinedCaseError


class Matrix(MatrixExpr):
    def __init__(self, s=None, size=(3, 3), value=None, attr=None):
        super().__init__()
        self.name = s
        self.size = size
        if value is None:
            self.value = np.empty(size, dtype='object')
        else:
            self.value = value
        self.attr = attr

    def __str__(self):
        return self.name

    def delta(self):
        if self.isOnes or self.isZero or self.isConstant:
            return Matrix('O', attr=['Constant', 'Zero'])
        else:
            from pydyn.operations.geometry import Delta
            return Delta(self)

    def variation_vector(self):
        return self.delta()

    def diff(self):
        if self.isConstant:
            return Matrix(s='0', size=self.size, attr=['Constant', 'Zero'])
        else:
            return Matrix(s='dot_' + self.name, size=self.size)

    def integrate(self):
        if self.isConstant:
            raise NotImplementedError
        else:
            s = self.name
            if 'dot_' in s:
                s.replace('dot_', '')
                return Matrix(s=s, size=self.size)
            else:
                return Matrix(s='int_' + s, size=self.size)


def getMatrices(input):
    if isinstance(input, list):
        vars = input
    elif isinstance(input, str):
        vars = input.split()
    else:
        return None
    s = []
    for v in vars:
        s.append(Matrix(v))
    return tuple(s)
