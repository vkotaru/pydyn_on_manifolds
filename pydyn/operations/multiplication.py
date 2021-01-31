from pydyn import Add, MAdd
from pydyn.base.matrices import Matrix, MatrixExpr
from pydyn.base.expr import Expr, Expression
from pydyn.base.scalars import ScalarExpr, Scalar
from pydyn.base.vectors import VectorExpr, Vector, ZeroVector
from pydyn.base.nodes import BinaryNode, NaryNode
from pydyn.operations.transpose import Transpose
from pydyn.utils.errors import ExpressionMismatchError, UndefinedCaseError


class Mul(NaryNode, ScalarExpr):
    """
    Scalar multiplication
    """

    def __init__(self, *args):
        super().__init__(*args)

        is_const = True
        is_zero = False
        for n in self.nodes:
            is_const = is_const and n.isConstant
            is_zero = is_zero or n.isZero
        self.isConstant = is_const
        self.isZero = is_zero

    def __str__(self):
        return super().get_str('')

    def copy(self):
        return Mul(self.nodes.copy())

    def delta(self):
        from pydyn.operations.addition import Add
        delta_ = Add()
        for i in range(self.n):
            if not self.nodes[i].isConstant:
                mul = self.copy()
                mul.replace_at(i, self.nodes[i].delta())
                delta_ += mul
        if delta_.n > 0:
            return delta_
        else:
            return ZeroVector

    def diff(self):
        from pydyn.operations.addition import Add
        diff_ = Add()
        for i in range(self.n):
            if not self.nodes[i].isConstant:
                mul = self.copy()
                mul.replace_at(i, self.nodes[i].diff())
                diff_ += mul
        if diff_.n > 0:
            return diff_
        else:
            return ZeroVector


class MVMul(BinaryNode, VectorExpr):
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
        self.isConstant = self.left.isConstant and self.right.isConstant
        self.isZero = self.left.isZero or self.right.isZero

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

    def delta(self):
        if self.left.isConstant and not self.right.isConstant:
            return MVMul(self.left, self.right.delta())
        elif not self.left.isConstant and self.right.isConstant:
            return MVMul(self.left.delta(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            return Vector('0', attr=['Constant', 'Zero'])
        else:
            return MVMul(self.left.delta(), self.right) + MVMul(self.left, self.right.delta())

    def diff(self):
        if self.left.isConstant and not self.right.isConstant:
            return MVMul(self.left, self.right.diff())
        elif not self.left.isConstant and self.right.isConstant:
            return MVMul(self.left.diff(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            return Vector('0', attr=['Constant', 'Zero'])
        else:
            return MVMul(self.left.diff(), self.right) + MVMul(self.left, self.right.diff())


class MMMul(BinaryNode, MatrixExpr):
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
        self.isConstant = self.left.isConstant and self.right.isConstant
        self.isZero = self.left.isZero or self.right.isZero

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

    def delta(self):
        if self.left.isConstant and not self.right.isConstant:
            return MMMul(self.left, self.right.delta())
        elif not self.left.isConstant and self.right.isConstant:
            return MMMul(self.left.delta(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            return Matrix('O', attr=['Constant', 'Zero'])
        else:
            return MMMul(self.left.delta(), self.right) + MMMul(self.left, self.right.delta())

    def diff(self):
        if self.left.isConstant and not self.right.isConstant:
            return MMMul(self.left, self.right.diff())
        elif not self.left.isConstant and self.right.isConstant:
            return MMMul(self.left.diff(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            return Matrix('O', attr=['Constant', 'Zero'])
        else:
            return MMMul(self.left.diff(), self.right) + MMMul(self.left, self.right.diff())


class SVMul(BinaryNode, VectorExpr):
    """
    Scalar-Vector multiplication
    """

    def __init__(self, l, r):
        super().__init__()
        if type(l) == float or type(l) == int:
            l = Scalar('(' + str(l) + ')', value=l, attr=['Constant'])
        if type(r) == float or type(r) == int:
            r = Scalar('(' + str(r) + ')', value=r, attr=['Constant'])
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
        self.isConstant = self.left.isConstant and self.right.isConstant
        self.isZero = self.left.isZero or self.right.isZero

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

    def delta(self):
        if self.left.isConstant and not self.right.isConstant:
            return SVMul(self.left, self.right.delta())
        elif not self.left.isConstant and self.right.isConstant:
            return SVMul(self.left.delta(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            return Vector('0', attr=['Constant', 'Zero'])
        else:
            return SVMul(self.left.delta(), self.right) + SVMul(self.left, self.right.delta())

    def diff(self):
        if self.left.isConstant and not self.right.isConstant:
            return SVMul(self.left, self.right.diff())
        elif not self.left.isConstant and self.right.isConstant:
            return SVMul(self.left.diff(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            return Vector('0', attr=['Constant', 'Zero'])
        else:
            return SVMul(self.left.diff(), self.right) + SVMul(self.left, self.right.diff())


class SMMul(BinaryNode, MatrixExpr):
    """
    Scalar-Matrix Multiplication
    """

    def __init__(self, l, r):
        super().__init__()
        if type(l) == float or type(l) == int:
            l = Scalar('(' + str(l) + ')', value=l, attr=['Constant'])
        if type(r) == float or type(r) == int:
            r = Scalar('(' + str(r) + ')', value=r, attr=['Constant'])

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
        self.isConstant = self.left.isConstant and self.right.isConstant
        self.isZero = self.left.isZero or self.right.isZero

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

    def delta(self):
        if self.left.isConstant and not self.right.isConstant:
            return SMMul(self.left, self.right.delta())
        elif not self.left.isConstant and self.right.isConstant:
            return SMMul(self.left.delta(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            return Matrix('O', attr=['Constant', 'Zero'])
        else:
            return SMMul(self.left.delta(), self.right) + SMMul(self.left, self.right.delta())

    def diff(self):
        if self.left.isConstant and not self.right.isConstant:
            return SMMul(self.left, self.right.diff())
        elif not self.left.isConstant and self.right.isConstant:
            return SMMul(self.left.diff(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            return Matrix('O', attr=['Constant', 'Zero'])
        else:
            return SMMul(self.left.diff(), self.right) + SMMul(self.left, self.right.diff())


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
        self.isConstant = self.left.isConstant and self.right.isConstant
        self.isZero = self.left.isZero or self.right.isZero

    def __str__(self):
        return self.left.__str__() + self.right.__str__()

    def __add__(self, other):
        if self.type == Expression.SCALAR:
            return Add(self, other)
        elif self.type == Expression.MATRIX:
            return MAdd(self, other)
        else:
            raise UndefinedCaseError

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

    def delta(self):
        if self.left.isConstant and not self.right.isConstant:
            return VVMul(self.left, self.right.delta())
        elif not self.left.isConstant and self.right.isConstant:
            return VVMul(self.left.delta(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            if self.type == Expression.SCALAR:
                return Scalar('0', attr=['Constant', 'Zero'])
            elif self.type == Expression.MATRIX:
                return Matrix('O', attr=['Constant', 'Zero'])
            else:
                raise UndefinedCaseError
        else:
            return VVMul(self.left.delta(), self.right) + VVMul(self.left, self.right.delta())

    def diff(self):
        if self.left.isConstant and not self.right.isConstant:
            return VVMul(self.left, self.right.diff())
        elif not self.left.isConstant and self.right.isConstant:
            return VVMul(self.left.diff(), self.right)
        elif self.left.isConstant and self.right.isConstant:
            if self.type == Expression.SCALAR:
                return Scalar('0', attr=['Constant', 'Zero'])
            elif self.type == Expression.MATRIX:
                return Matrix('O', attr=['Constant', 'Zero'])
            else:
                raise UndefinedCaseError
        else:
            return VVMul(self.left.diff(), self.right) + VVMul(self.left, self.right.diff())
