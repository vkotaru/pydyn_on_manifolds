from pydom.variables.variables import MatrixExpr, ScalarExpr, VectorExpr
from pydom.utils.errors import ExpressionMismatchError
from pydom.variables import Variable, Expr

class Mul(Expr):
    def __init__(self, l=Variable(), r=Variable):
        super().__init__()

        if l.__type__ == type(MatrixExpr()):
            if r.__type__ == type(MatrixExpr()):
                """Matrix Matrix Multiplication is a Matrix"""
                self.define(l, r, r.__type__)
            
            elif r.__type__ == type(VectorExpr()):
                """Matrix Vector Multiplication is a Vector"""
                self.define(l, r, r.__type__)

            elif r.__type__ == type(ScalarExpr()):
                """Matrix Scalar Multiplication is a Matrix"""
                self.define(l, r, l.__type__)

        # elif l.__type__ == type(VectorExpr()):
        #     if r.__type__ == type()


    def define(self, l, r, t):
        self._left = l
        self._right = r
        self.__type__ = t