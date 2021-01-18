from pydyn.data_types.expr import Expr, Expression
from pydyn.data_types.scalars import ScalarExpr, Scalar
from pydyn.data_types.vectors import VectorExpr
from pydyn.operations.nodes import BinaryNode
from pydyn.operations.transpose import Transpose
from pydyn.utils.errors import ExpressionMismatchError, UndefinedCaseError


class Mul(ScalarExpr, BinaryNode):
    """
    Scalar multiplication
    """

    def __init__(self, l, r):
        super().__init__()
        if type(l) == float or type(l) == int:
            l = Scalar('(' + str(l) + ')', attr=['Constant'])
        if type(r) == float or type(r) == int:
            r = Scalar('(' + str(r) + ')', attr=['Constant'])
        if l.type == Expression.SCALAR and r.type == Expression.SCALAR:
            self.left = l
            self.right = r
            self.type = l.type
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self.left.__str__() + self.right.__str__()
        return str

    def delta(self):
        if self.left.isConstant and not self.right.isConstant:
            return Mul(self.left, self.right.delta())
        elif not self.left.isConstant and self.right.isConstant:
            return Mul(self.left.delta(), self.right)
        elif self.right.isConstant and self.right.isConstant:
            return Scalar('0', attr=['Constant', 'Zero'])
        else:
            Mul(self.left.delta(), self.right) + Mul(self.left, self.right.delta())


class MVMul(VectorExpr, BinaryNode):
    """
    Matrix-Vector multiplication
    """

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.MATRIX and r.type == Expression.VECTOR:
            self.left = l
            self.right = r
            self.type = Expression.VECTOR
        elif l.type == Expression.VECTOR and r.type == Expression.MATRIX:
            if type(l) == type(Transpose()):
                self.left = l
                self.right = r
                self.type = Expression.VECTOR
            else:
                raise ExpressionMismatchError
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self.left.__str__() + self.right.__str__()
        return str

    def __mul__(self, other):
        if other.type == Expression.SCALAR:
            return SVMul(self, other)
        elif other.type == Expression.VECTOR:
            return VVMul(self, other)
        elif other.type == Expression.MATRIX:
            return MVMul(self, other)


class MMMul(Expr, BinaryNode):
    """
    Matrix-Matrix multiplication
    """

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.MATRIX and r.type == Expression.MATRIX:
            self.left = l
            self.right = r
            self.type = Expression.MATRIX
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self.left.__str__() + self.right.__str__()
        return str

    def __mul__(self, other):
        if other.type == Expression.SCALAR:
            return SMMul(self, other)
        elif other.type == Expression.VECTOR:
            return MVMul(self, other)
        elif other.type == Expression.MATRIX:
            return MMMul(self, other)


class SVMul(Expr, BinaryNode):
    """
    Scalar-Vector multiplication
    """

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.VECTOR and r.type == Expression.SCALAR:
            self.left = l
            self.right = r
            self.type = Expression.VECTOR
        elif l.type == Expression.SCALAR and r.type == Expression.VECTOR:
            self.left = r
            self.right = l
            self.type = Expression.VECTOR
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self.left.__str__() + self.right.__str__()
        return str

    def __mul__(self, other):
        if __name__ == '__main__':
            if other.type == Expression.SCALAR:
                return SVMul(self, other)
            elif other.type == Expression.VECTOR:
                return VVMul(self, other)
            elif other.type == Expression.MATRIX:
                return MVMul(self, other)


class SMMul(Expr, BinaryNode):
    """
    Scalar-Matrix Multiplication
    """

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.MATRIX and r.type == Expression.SCALAR:
            self.left = l
            self.right = r
            self.type = Expression.MATRIX
        elif l.type == Expression.SCALAR and r.type == Expression.MATRIX:
            self.left = r
            self.right = l
            self.type = Expression.MATRIX
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self.left.__str__() + self.right.__str__()
        return str

    def __mul__(self, other):
        if other.type == Expression.SCALAR:
            return SMMul(self, other)
        elif other.type == Expression.VECTOR:
            return MVMul(self, other)
        elif other.type == Expression.MATRIX:
            return MMMul(self, other)
        else:
            raise UndefinedCaseError


class VVMul(Expr, BinaryNode):
    """
    Vector Vector Multiplication
    """

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.VECTOR and r.type == Expression.VECTOR:
            if type(l) == type(Transpose(None)) and type(r) != type(Transpose(None)):
                self.left = l
                self.right = r
                self.type = Expression.SCALAR
            elif type(l) != type(Transpose(None)) and type(r) == type(Transpose(None)):
                self.left = l
                self.right = r
                self.type = Expression.MATRIX
            else:
                raise ExpressionMismatchError
        else:
            raise ExpressionMismatchError

    def __str__(self):
        return self.left.__str__() + self.right.__str__()

    def __mul__(self, other):
        if self.type == Expression.SCALAR:
            if other.type == Expression.SCALAR:
                return Mul(self, other)
            elif other.type == Expression.VECTOR:
                return SVMul(self, other)
            elif other.type == Expression.MATRIX:
                return SMMul(self, other)
            else:
                raise UndefinedCaseError
        elif self.type == Expression.MATRIX:
            if other.type == Expression.SCALAR:
                return SMMul(self, other)
            elif other.type == Expression.VECTOR:
                return MVMul(self, other)
            elif other.type == Expression.MATRIX:
                return MMMul(self, other)
            else:
                raise UndefinedCaseError
        else:
            raise UndefinedCaseError
