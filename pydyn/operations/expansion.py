from pydyn.operations.binary_tree import has_nested_add
from pydyn.operations.geometry import Dot, Cross, Vee
from pydyn.operations.addition import Add, VAdd, MAdd
from pydyn.operations.multiplication import Mul, SMMul, SVMul, MVMul, VVMul, MMMul
from pydyn.data_types.matrices import MatrixExpr
from pydyn.data_types.scalars import ScalarExpr
from pydyn.data_types.vectors import VectorExpr
from pydyn.utils.errors import UndefinedCaseError


def expand_scalar(expr):
    if isinstance(expr, Add):
        return Add(expand(expr.left), expand(expr.right))

    elif isinstance(expr, Mul):
        if isinstance(expr.left, Add) and isinstance(expr.right, Add):
            """(a+b)(c+d) = ac + ad + bc + bd"""
            a, b = expr.left.left, expr.left.right
            c, d = expr.right.left, expr.right.right
            return expand(a * c) + expand(a * d) + expand(b * c) + expand(b * d)

        elif isinstance(expr.left, Add):
            """(a+b)c = ac + bc"""
            a, b = expr.left.left, expr.left.right
            c = expr.right
            return expand(a * c) + expand(b * c)

        elif isinstance(expr.right, Add):
            """a(b+c) = ab + ac"""
            a = expr.left
            b, c = expr.right.left, expr.right.right
            return expand(a * b) + expand(a * c)
            pass

        else:
            if has_nested_add(expr):
                return expand(expand(expr.left) * expand(expr.right))
            else:
                return expr

    elif isinstance(expr, Dot):
        if isinstance(expr.left, VAdd) and isinstance(expr.right, VAdd):
            """(x+y).(u+v) = x.u + x.v + y.u + y.v"""
            x, y = expr.left.left, expr.left.right
            u, v = expr.right.left, expr.right.right
            return expand(Dot(x, u)) + expand(Dot(x, v)) + expand(Dot(y, u)) + expand(Dot(y, v))

        elif isinstance(expr.right, VAdd):
            """x.(u+v) = x.u + x.v"""
            x = expr.left
            u, v = expr.right.left, expr.right.right
            return expand(Dot(x, u)) + expand(Dot(x, v))

        elif isinstance(expr.left, VAdd):
            """(x+y).u = x.u + y.u"""
            x, y = expr.left.left, expr.left.right
            u = expr.right
            return expand(Dot(x, u)) + expand(Dot(y, u))

        else:
            if has_nested_add(expr):
                return expand(Dot(expand(expr.left), expand(expr.right)))
            else:
                return expr

    elif isinstance(expr, VVMul):
        raise NotImplementedError

    return expr


def expand_vector(expr):
    if isinstance(expr, VAdd):
        return expand(expr.left) + expand(expr.right)

    elif isinstance(expr, MVMul):
        if isinstance(expr.left, MAdd):
            """(A+B)x = Ax+Bx"""
            return expand(MVMul(expr.left.left, expr.right)) + expand(MVMul(expr.left.right, expr.right))
        elif isinstance(expr.right, VAdd):
            """A(x+y) = Ax + Ay"""
            return expand(MVMul(expr.left, expr.right.left)) + expand(MVMul(expr.left, expr.right.right))
        else:
            if has_nested_add(expr):
                return expand(MVMul(expand(expr.left), expand(expr.right)))
            else:
                return expr

    elif isinstance(expr, SVMul):
        if isinstance(expr.left, VAdd):
            """(x+y)a=xa+ya"""
            return expand(SVMul(expr.left.left, expr.right) + SVMul(expr.left.right, expr.right))
        else:
            if has_nested_add(expr):
                return expand(SVMul(expand(expr.left), expand(expr.right)))
            else:
                return expr
        pass

    elif isinstance(expr, Cross):
        if isinstance(expr.left, VAdd) and isinstance(expr.right, VAdd):
            x, y = expr.left.left, expr.left.right
            u, v = expr.right.left, expr.right.right
            return expand(Cross(x, u)) + expand(Cross(x, v)) + expand(Cross(y, u)) + expand(Cross(y, v))
        elif isinstance(expr.left, VAdd):
            return expand(Cross(expr.left.left, expr.right)) + expand(Cross(expr.left.right, expr.right))
        elif isinstance(expr.right, VAdd):
            return expand(Cross(expr.left, expr.right.left)) + expand(Cross(expr.left, expr.right.right))
        else:
            if has_nested_add(expr):
                return expand(Cross(expand(expr.left), expand(expr.right)))
            else:
                return expr

    elif isinstance(expr, Vee):
        return Vee(expand(expr))

    return expr


def expand_matrix(expr):
    if isinstance(expr, MAdd):
        return MAdd(expand(expr.left), expand(expr.right))

    elif isinstance(expr, MMMul):
        if isinstance(expr.left, MAdd):
            return expand(MMMul(expr.left.left, expr.right)) + expand(MMMul(expr.left.right, expr.right))

        elif isinstance(expr.right, MAdd):
            return expand(MMMul(expr.left, expr.right.left)) + expand(MMMul(expr.left, expr.right.right))

        else:
            if has_nested_add(expr):
                return expand(MMMul(expand(expr.left), expand(expr.right)))
            else:
                return expr

    elif isinstance(expr, SMMul):
        pass

    elif isinstance(expr, VVMul):
        raise NotImplementedError

    return expr


def expand(expr):
    # TODO add expand functionality to the Expr class directly
    if isinstance(expr, ScalarExpr):
        return expand_scalar(expr)
    elif isinstance(expr, VectorExpr):
        return expand_vector(expr)
    elif isinstance(expr, MatrixExpr):
        return expand_matrix(expr)
    else:
        raise UndefinedCaseError
