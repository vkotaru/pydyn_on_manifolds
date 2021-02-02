class UnaryNode(object):
    """
    Unary node used by transpose, hat, vee, and such operators
    """

    def __init__(self):
        super().__init__()
        self._expr = None

    @property
    def expr(self):
        return self._expr

    @expr.setter
    def expr(self, e):
        self._expr = e

    def has(self, elem):
        return elem.__str__() == self.__str__()


class BinaryNode(object):
    """
    Binary Node used by addition, multiplication, dot, cross and other operators
    """

    def __init__(self):
        super().__init__()
        self._left = None
        self._right = None

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, l):
        self._left = l

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, r):
        self._right = r

    def has(self, elem):
        return self.left.has(elem) or self.right.has(elem)
