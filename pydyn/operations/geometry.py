from pydyn.operations.addition import Add
from pydyn.data_types.expr import Expr, Expression
from pydyn.operations.nodes import UnaryNode, BinaryNode
from pydyn.operations.multiplication import Mul, SMMul, SVMul
from pydyn.utils.errors import UndefinedCaseError, ExpressionMismatchError


class Delta(Expr, UnaryNode):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
        self.type = expr.type

    def __str__(self):
        return 'delta{' + self.expr.__str__() + '}'


class Dot(Expr, BinaryNode):
    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.VECTOR and r.type == Expression.VECTOR:
            self.left = l
            self.right = r
            self.type = Expression.SCALAR
        else:
            raise ExpressionMismatchError

    def __str__(self):
        return 'Dot(' + self.left.__str__() + ',' +self.right.__str__() + ')'

    def __mul__(self, other):
        if other.type == Expression.SCALAR:
            return Mul(self, other)
        elif other.type == Expression.VECTOR:
            return SVMul(self, other)
        elif other.type == Expression.MATRIX:
            return SMMul(self, other)
        else:
            raise UndefinedCaseError

    def __add__(self, other):
        return Add(self, other)



class Cross(Expr, BinaryNode):
    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.VECTOR and r.type == Expression.VECTOR:
            self.left = l
            self.right = r
            self.type = Expression.VECTOR
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError

    def __str__(self):
        return 'Cross(' + self.left.__str__() + ',' +self.right.__str__() + ')'


class Hat(Expr, UnaryNode):
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


class Vee(Expr, UnaryNode):
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