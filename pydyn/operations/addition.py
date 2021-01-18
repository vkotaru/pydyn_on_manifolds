from pydyn.data_types.expr import Expression, Expr
from pydyn.operations.nodes import BinaryNode
from pydyn.utils.errors import ExpressionMismatchError
import pydyn.data_types


class Add(Expr, BinaryNode):
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


class VAdd(Expr, BinaryNode):
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


class MAdd(Expr, BinaryNode):
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
