from pydyn.data_types.expr import Expression, Expr
from pydyn.data_types.matrices import MatrixExpr
from pydyn.data_types.scalars import ScalarExpr, Scalar
from pydyn.data_types.vectors import VectorExpr
from pydyn.operations.nodes import BinaryNode
from pydyn.utils.errors import ExpressionMismatchError
import pydyn.data_types


class Add(ScalarExpr, BinaryNode):
    """Scalar Addition"""

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.SCALAR and r.type == Expression.SCALAR:
            self._left = l
            self._right = r
            self.type = l.type
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = '(' + self._left.__str__() + '+' + self._right.__str__() + ')'
        return str

    def __add__(self, other):
        if other.type == Expression.SCALAR:
            return Add(self, other)
        else:
            raise ExpressionMismatchError('Add', self.type, other.type)

    def delta(self):
        if self.left.isConstant and not self.right.isConstant:
            return self.right.delta()
        elif not self.left.isConstant and self.right.isConstant:
            return self.left.delta()
        elif self.left.isConstant and self.right.isConstant:
            return Scalar('0', attr=['Constant', 'Zero'])
        else:
            Add(self.left.delta(), self.right.delta())


class VAdd(VectorExpr, BinaryNode):
    """Vector Addition"""

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.VECTOR and r.type == Expression.VECTOR:
            self._left = l
            self._right = r
            self.type = l.type
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = '(' + self._left.__str__() + '+' + self._right.__str__() + ')'
        return str

    def __add__(self, other):
        if other.type == Expression.VECTOR:
            return VAdd(self, other)
        else:
            raise ExpressionMismatchError('VAdd', self.type, other.type)


class MAdd(MatrixExpr, BinaryNode):
    """Matrix Addition"""

    def __init__(self, l, r):
        super().__init__()
        if l.type == Expression.MATRIX and r.type == Expression.MATRIX:
            self._left = l
            self._right = r
            self.type = l.type
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = '(' + self._left.__str__() + '+' + self._right.__str__() + ')'
        return str

    def __add__(self, other):
        if other.type == Expression.MATRIX:
            return MAdd(self, other)
        else:
            raise ExpressionMismatchError('MAdd', self.type, other.type)
