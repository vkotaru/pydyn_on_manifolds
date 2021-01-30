import numpy as np
from pydyn.data_types.expr import Expression, Expr, Manifold
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
        from pydyn.data_types.scalars import Scalar
        if type(other) == float or type(other) == int:
            other = Scalar('(' + str(other) + ')', value=other, attr=['Constant'])
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
        if attr is None:
            self.attr = []
        else:
            self.attr = attr
        if 'SymmetricMatrix' in self.attr:
            self.isSymmetric = True
        else:
            self.isSymmetric = False

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


class SkewSymmMatrix(Matrix):
    def __init__(self):
        super().__init__()
        self.attr.append('SkewSymmetry')


class SO3(Matrix, Manifold):
    def __init__(self, s=None, size=(3, 3), value=None, attr=None):
        super().__init__(s, size, value, attr)
        super(Manifold, self).__init__()
        self.tangent_vector = '\\Omega_{' + self.name + '}'
        self.variation_vector = '\\eta_{' + self.name + '}'
        if attr is None:
            attr = []
        attr.append('Manifold')
        self.attr = attr

    def delta(self):
        from pydyn.operations.multiplication import MMMul
        from pydyn.operations.geometry import Hat
        return MMMul(self, Hat(self.get_variation_vector()))

    def get_tangent_vector(self):
        from pydyn.data_types.vectors import TSO3
        return TSO3(self.tangent_vector, SO3=self)

    def get_variation_vector(self):
        from pydyn.data_types.vectors import Vector
        return Vector(self.variation_vector)

    def diff(self):
        from pydyn.operations.multiplication import MMMul
        from pydyn.operations.geometry import Hat
        return MMMul(self, Hat(self.get_tangent_vector()))


ZeroMatrix = Matrix('0', attr=['Constant', 'Zero'])
IdentityMatrix = Matrix('I', attr=['Constant', 'Identity'])

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
