import pydyn.data_types
from pydyn.operations.transpose import Transpose
from pydyn.utils.errors import ExpressionMismatchError, UndefinedCaseError


class Mul(object):
    def __init__(self, l, r):
        if l.type == 'ScalarExpr' and r.type == 'ScalarExpr':
            self._left = l
            self._right = r
            self.type = l.type
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self._left.__str__() + self._right.__str__()
        return str


class MVMul(object):
    def __init__(self, l, r):
        if l.type == 'MatrixExpr' and r.type == 'VectorExpr':
            self._left = l
            self._right = r
            self.type = 'VectorExpr'
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self._left.__str__() + self._right.__str__()
        return str


class MMMul(object):
    def __init__(self, l, r):
        if l.type == 'MatrixExpr' and r.type == 'MatrixExpr':
            self._left = l
            self._right = r
            self.type = 'MatrixExpr'
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self._left.__str__() + self._right.__str__()
        return str


class SVMul(object):
    def __init__(self, l, r):
        if l.type == 'VectorExpr' and r.type == 'ScalarExpr':
            self._left = l
            self._right = r
            self.type = 'VectorExpr'
        elif l.type == 'ScalarExpr' and r.type == 'VectorExpr':
            self._left = r
            self._right = l
            self.type = 'VectorExpr'
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self._left.__str__() + self._right.__str__()
        return str


class SMMul(object):
    def __init__(self, l, r):
        if l.type == 'MatrixExpr' and r.type == 'ScalarExpr':
            self._left = l
            self._right = r
            self.type = 'MatrixExpr'
        elif l.type == 'ScalarExpr' and r.type == 'MatrixExpr':
            self._left = r
            self._right = l
            self.type = 'MatrixExpr'
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self._left.__str__() + self._right.__str__()
        return str

class VVMul(object):
    def __init__(self, l, r):
        if l.type == 'VectorExpr' and r.type == 'VectorExpr':
            if type(l) == type(Transpose(None)) and type(r) != type(Transpose(None))  :
                self._left = l
                self._right = r
                self.type = 'ScalarExpr'
            elif type(l) != type(Transpose(None)) and type(r) == type(Transpose(None))  :
                self._left = l
                self._right = r
                self.type = 'MatrixExpr'
            else:
                raise ExpressionMismatchError
        else:
            raise ExpressionMismatchError