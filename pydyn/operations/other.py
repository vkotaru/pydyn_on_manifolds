import pydyn.data_types


class Delta(object):
    def __init__(self, expr):
        self.expr = expr
        self.type = expr.type

    def __str__(self):
        return 'delta{' + self.expr.__str__() + '}'


class Dot(object):
    def __init__(self, l, r):
        if l.type == 'VectorExpr' and r.type == 'VectorExpr':
            self._left = l
            self._right = r
            self.type = 'ScalarExpr'
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError

    def __str__(self):
        return 'Dot(' + self._left.__str__() + ',', +self._right.__str__() + ')'


class Cross(object):
    def __init__(self, l, r):
        if l.type == 'VectorExpr' and r.type == 'VectorExpr':
            self._left = l
            self._right = r
            self.type = 'VectorExpr'
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError

    def __str__(self):
        return '(' + self._left.__str__() + 'x', +self._right.__str__() + ')'


class Hat(object):
    def __init__(self, expr):
        if expr.type == 'VectorExpr':
            self.expr = expr
            self.type = 'MatrixExpr'
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError

    def __str__(self):
        return 'Hat(' + self.expr.__str__() + ')'


class Vee(object):
    def __init__(self, expr):
        if expr.type == 'MatrixExpr':  # ideally this should be skew-symmetric matrix
            self.expr = expr
            self.type = 'VectorExpr'
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError

    def __str__(self):
        return 'Vee(' + self.expr.__str__() + ')'
