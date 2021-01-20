from pydyn.data_types.vectors import Vector
from pydyn.data_types.expr import Expression
from pydyn.utils.errors import UndefinedCaseError
from pydyn.operations.addition import Add, VAdd, MAdd
from pydyn.operations.multiplication import Mul, SVMul, SMMul, VVMul, MVMul, MMMul
from pydyn.operations.geometry import Dot


def extract_coeff(expr, sym):
    if expr.type == Expression.SCALAR:
        return efs(expr, sym)

    elif expr.type == Expression.VECTOR:
        raise NotImplementedError

    elif expr.type == Expression.MATRIX:
        raise NotImplementedError
    else:
        raise UndefinedCaseError


def efs(expr, vec):
    """Extract From Scalar"""
    # Add
    if isinstance(expr, Add):
        if expr.left.has(vec) and expr.right.has(vec):
            return VAdd(efs(expr.left, vec), efs(expr.right, vec))
        elif expr.left.has(vec):
            return efs(expr.left, vec)
        elif expr.right.has(vec):
            return efs(expr.right, vec)
        else:
            return Vector('0', attr=['Constant', 'Zero'])

    elif isinstance(expr, Mul):
        if expr.left.has(vec) and expr.right.has(vec):
            raise NotImplementedError
        elif expr.left.has(vec):
            return SVMul(efs(expr.left, vec), expr.right)
        elif expr.right.has(vec):
            return SVMul(efs(expr.right, vec), expr.left)
        else:
            return Vector('0', attr=['Constant', 'Zero'])

    elif isinstance(expr, Dot):
        if expr.left.has(vec) and expr.right.has(vec):
            raise NotImplementedError
        elif expr.left.has(vec):
            if expr.left == vec:
                return expr.right
            else:
                raise NotImplementedError
        elif expr.right.has(vec):
            if expr.right == vec:
                return expr.left
            else:
                raise NotImplementedError
        else:
            return Vector('0', attr=['Constant', 'Zero'])

    return expr
