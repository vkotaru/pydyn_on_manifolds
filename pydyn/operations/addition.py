from pydyn.utils.errors import ExpressionMismatchError
import pydyn.data_types


class Add(object):
    """Scalar Addition"""

    def __init__(self, l, r):
        if l.type == 'ScalarExpr' and r.type == 'ScalarExpr':
            self._left = l
            self._right = r
            self.type = l.type
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = '(' + self._left.__str__() + '+' + self._right.__str__() + ')'
        return str


class VAdd(object):
    """Vector Addition"""

    def __init__(self, l, r):
        if l.type == 'VectorExpr' and r.type == 'VectorExpr':
            self._left = l
            self._right = r
            self.type = l.type
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = '(' + self._left.__str__() + '+' + self._right.__str__() + ')'
        return str


class MAdd(object):
    """Matrix Addition"""

    def __init__(self, l, r):
        if l.type == 'MatrixExpr' and r.type == 'MatrixExpr':
            self._left = l
            self._right = r
            self.type = l.type
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = '(' + self._left.__str__() + '+' + self._right.__str__() + ')'
        return str
