import numpy as np
from pydyn.data_types.expr import Expression, Expr
from pydyn.utils.errors import ExpressionMismatchError, UndefinedCaseError


class VectorExpr(Expr):
    def __init__(self):
        super().__init__()
        self.type = Expression.VECTOR

    def __str__(self):
        raise NotImplementedError

    def __add__(self, other):
        from pydyn.operations.addition import VAdd
        if other.type == Expression.VECTOR:
            return VAdd(self, other)
        else:
            raise ExpressionMismatchError

    def __mul__(self, other):
        from pydyn.operations.multiplication import SVMul, VVMul, MVMul
        from pydyn.data_types.scalars import Scalar
        if type(other) == float or type(other) == int:
            other = Scalar('(' + str(other) + ')', value=other, attr=['Constant'])
        if other.type == Expression.SCALAR:
            return SVMul(self, other)
        elif other.type == Expression.VECTOR:
            return VVMul(self, other)
        elif other.type == Expression.MATRIX:
            return MVMul(self, other)
        else:
            return UndefinedCaseError

    def dot(self, other):
        from pydyn.operations.geometry import Dot

        return Dot(self, other)

    def cross(self, other):
        from pydyn.operations.geometry import Cross

        return Cross(self, other)


class Vector(VectorExpr):
    def __init__(self, s, size=(3,), value=None, attr=None):
        super().__init__()
        self.name = s
        self.size = size
        if value is None:
            self.value = np.empty(size, dtype='object')
        else:
            self.value = value
            self.size = self.value.shape
        self.attr = attr  # Constant, Zero, Ones

    def __str__(self):
        return self.name

    def delta(self):
        if self.isOnes or self.isZero or self.isConstant:
            return Vector('0', attr=['Constant', 'Zero'])
        else:
            from pydyn.operations.geometry import Delta
            return Delta(self)

    def diff(self):
        if self.isConstant:
            return Vector(s='0', size=self.size, attr=['Constant', 'Zero'])
        else:
            return Vector(s='dot_' + self.name, size=self.size)

    def variation_vector(self):
        return self.delta()

    def integrate(self):
        if self.isConstant:
            raise NotImplementedError
        else:
            s = self.name
            if 'dot_' in s:
                new_s = s.replace("dot_", "")
                return Vector(s=new_s, size=self.size)
            else:
                return Vector(s='int_' + s, size=self.size)


class TSO3(Vector):
    """TSO(3) Tangent space of SO3 manifold"""
    def __init__(self, s, SO3=None):
        super().__init__(s, value=None, attr=None)
        self.SO3 = SO3
        self.attr.append('TangentVector')

    def delta(self):
        from pydyn.operations.geometry import Hat
        eta = self.SO3.get_variation_vector()
        return Hat(self) * eta + eta.diff()


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
