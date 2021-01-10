from pydom.utils.errors import ExpressionMismatchError
from pydom.variables import Variable, Expr


class Add(Expr):
    def __init__(self, l=Variable(), r=Variable()):
        super().__init__()
        if (l.__type__ == r.__type__):
            self._left = l
            self._right = r
            self.__type__ = l.__type__
        else:
            raise ExpressionMismatchError

    def __str__(self):
        str = self._left.__str__() + '+' + self._right.__str__()
        return str
