from pydyn.operations.transpose import Transpose
from pydyn.data_types.matrices import MatrixExpr
from pydyn.data_types.scalars import ScalarExpr, Scalar
from pydyn.data_types.vectors import VectorExpr, Vector
from pydyn.data_types.expr import Expr, Expression
from pydyn.operations.nodes import UnaryNode, BinaryNode
from pydyn.utils.errors import UndefinedCaseError, ExpressionMismatchError


class Delta(Expr, UnaryNode):
    """
    Variation operator
    """

    def __init__(self, expr):
        super().__init__()
        self.expr = expr
        self.type = expr.type

    def __str__(self):
        return '\delta{' + self.expr.__str__() + '}'

    def __mul__(self, other):
        from pydyn.operations.multiplication import Mul, SVMul, SMMul, VVMul, MVMul, MMMul
        if type(other) == float or type(other) == int:
            other = Scalar('(' + str(other) + ')', value=other, attr=['Constant'])
        if self.type == Expression.SCALAR:
            if other.type == Expression.SCALAR:
                return Mul(self, other)
            elif other.type == Expression.VECTOR:
                return SVMul(other, self)
            elif other.type == Expression.MATRIX:
                return SMMul(other, self)
            else:
                raise UndefinedCaseError

        elif self.type == Expression.VECTOR:
            if other.type == Expression.SCALAR:
                return SVMul(self, other)
            elif other.type == Expression.VECTOR:
                return VVMul(self, other)
            elif other.type == Expression.MATRIX:
                return MVMul(self, other)
            else:
                return UndefinedCaseError

        elif self.type == Expression.MATRIX:
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
        else:
            raise UndefinedCaseError

    def __add__(self, other):
        return self.expr.__add__(other)

    def diff(self):
        return Delta(self.expr.diff())

    def integrate(self):
        return Delta(self.expr.integrate())


class Dot(ScalarExpr, BinaryNode):
    """
    Dot product of vectors
    """

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.VECTOR and r.type == Expression.VECTOR:
            self.left = l
            self.right = r
            self.type = Expression.SCALAR
        else:
            raise ExpressionMismatchError
        self.isConstant = self.left.isConstant and self.right.isConstant
        if self.left.isZero or self.right.isZero:
            self.isConstant = True
        self.isZero = self.left.isZero or self.right.isZero

    def __str__(self):
        return 'Dot(' + self.left.__str__() + ',' + self.right.__str__() + ')'

    def delta(self):
        from pydyn.operations.multiplication import MVMul, Mul
        from pydyn.operations.addition import Add
        if isinstance(self.right, MVMul):
            if self.right.left.isSymmetric and self.left == self.right.right:
                return Add(Dot(self.left.delta(), self.right)*2, Dot(self.left, MVMul(self.right.left.delta(), self.right.right)))
            else:
                return Add(Dot(self.left.delta(), self.right), Dot(self.left, self.right.delta()))
        else:
            if self.left.isConstant and not self.right.isConstant:
                return Dot(self.left, self.right.delta())
            elif not self.left.isConstant and self.right.isConstant:
                return Dot(self.left.delta(), self.right)
            elif self.left.isConstant and self.right.isConstant:
                return Vector('0', attr=['Constant', 'Zero'])
            elif self.left == self.right:
                return Dot(self.left.delta(), self.right) * 2
            else:
                return Add(Dot(self.left.delta(), self.right), Dot(self.left, self.right.delta()))


class Cross(VectorExpr, BinaryNode):
    """
    Cross product of 3x1 vectors
    """

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.VECTOR and r.type == Expression.VECTOR:
            self.left = l
            self.right = r
            self.type = Expression.VECTOR
        else:
            raise ExpressionMismatchError
        self.isZero = self.left.isZero or self.left.isZero

    def __str__(self):
        return 'Cross(' + self.left.__str__() + ',' + self.right.__str__() + ')'


class Hat(MatrixExpr, UnaryNode):
    """
    Hat map: Rn to LieGroup G
    """

    def __init__(self, expr):
        super().__init__()
        if expr.type == Expression.VECTOR:
            self.expr = expr
            self.type = Expression.MATRIX
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError

    def __str__(self):
        return 'Hat(' + self.expr.__str__() + ')'


class Vee(MatrixExpr, UnaryNode):
    """Vee map: LieGroup G to Rn"""

    def __init__(self, expr):
        super().__init__()
        if expr.type == Expression.MATRIX:  # ideally this should be skew-symmetric matrix
            self.expr = expr
            self.type = Expression.VECTOR
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError

    def __str__(self):
        return 'Vee(' + self.expr.__str__() + ')'
