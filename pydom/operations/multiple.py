from pydom.variables.variables import MatrixExpr, ScalarExpr, VectorExpr, Variable, Expr
from pydom.variables.vectors import Vector
from pydom.operations import Add
from pydom.utils.errors import ExpressionMismatchError, UndefinedCaseError

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
        
        elif l.__type__== type(VectorExpr()):
            if type(l) == type(Transpose()):
                if r.__type__ == type(MatrixExpr()):
                    """Transpose Vector and Matrix Multiplication is Transpose Vector"""
                    self.define(l, r, type(VectorExpr()))

                elif r.__type__ == type(VectorExpr()):
                    if type(r) == type(Transpose()):
                        raise ExpressionMismatchError('Multiplication', 'TransposeVector', 'TransposeVector')
                    else:
                        """Transpose Vector and Vector Multiplication is Scalar"""
                        self.define(l, r, type(ScalarExpr()))

                elif r.__type__ == type(ScalarExpr()):
                    """Transpose Vector and a Scalar Multiplication is transpose vector"""
                    self.define(l, r, type(VectorExpr()))
                
                else:
                    raise UndefinedCaseError
            
            else:
                if r.__type__ == type(MatrixExpr()):
                    raise ExpressionMismatchError('Multiplication', 'Vector', 'Matrix')

                elif r.__type__ == type(VectorExpr()):
                    if type(r) == type(Transpose()):
                        """Vector and Vector Transpose Multiplication is a Matrix"""
                        self.define(l, r, type(MatrixExpr()))

                    else:
                        raise ExpressionMismatchError('Multiplication', 'Vector', 'Vector')

                elif r.__type__ == type(ScalarExpr()):
                    """Vector and a Scalar Multiplication is vector"""
                    self.define(l, r, type(VectorExpr()))

        elif l.__type__== type(ScalarExpr()):
            if r.__type__ == type(MatrixExpr()):
                self.define(r, l, type(MatrixExpr()))
            
            elif r.__type__ == type(VectorExpr()):
                self.define(r, l, type(VectorExpr()))

            elif r.__type__ == type(ScalarExpr()):
                self.define(r, l, type(ScalarExpr()))

        else:
            raise UndefinedCaseError()


        # elif l.__type__ == type(VectorExpr()):
        #     if r.__type__ == type()


    def define(self, l, r, t):
        self._left = l
        self._right = r
        self.__type__ = t

    def __str__(self):
        str = self._left.__str__() + self._right.__str__()
        return str