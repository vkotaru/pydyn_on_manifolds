from pydyn.operations.addition import Add, MAdd
from pydyn.operations.binary_tree import has_nested_scalars
from pydyn.operations.multiplication import Mul, SVMul, MVMul, SMMul, MMMul
from pydyn.operations.geometry import Dot, Cross
from pydyn.data_types.matrices import MatrixExpr
from pydyn.data_types.scalars import ScalarExpr
from pydyn.data_types.vectors import VectorExpr
from pydyn.operations.expansion import expand


def pull(expr):
    if isinstance(expr, ScalarExpr):
        if isinstance(expr, Add):
            return pull(expr.left) + pull(expr.right)
        elif isinstance(expr, Mul):
            return pull(expr.left) * pull(expr.right)
        elif isinstance(expr, Dot):
            if isinstance(expr.left, SVMul):
                return pull(expr.left.right * Dot(expr.left.left, expr.right))
            elif isinstance(expr.right, SVMul):
                return pull(expr.right.right * Dot(expr.right.left, expr.left))
            else:
                if has_nested_scalars(expr):
                    return pull(Dot(pull(expr.left), pull(expr.right)))
                else:
                    return expr
        else:
            return expr

    elif isinstance(expr, VectorExpr):
        if isinstance(expr, MVMul):
            if isinstance(expr.left, SMMul):
                return pull(SVMul(MVMul(expr.left.left, expr.right), expr.left.right))
            elif isinstance(expr.right, SVMul):
                return pull(SVMul(MVMul(expr.left, expr.right.left), expr.right.right))
            else:
                if has_nested_scalars(expr):
                    return pull(MVMul(pull(expr.left), pull(expr.right)))
                else:
                    return expr
        elif isinstance(expr, SVMul):
            if isinstance(expr.left, SVMul):
                return pull(SVMul(expr.left.left, expr.left.right * expr.right))
            else:
                if has_nested_scalars(expr):
                    return pull(SVMul(pull(expr.left), pull(expr.right)))
                else:
                    return expr
        elif isinstance(expr, Cross):
            if isinstance(expr.left, SVMul) and isinstance(expr.right, SVMul):
                return pull(SVMul(Cross(expr.left.left, expr.right.left), expr.left.right * expr.right.right))
            elif isinstance(expr.left, SVMul):
                return pull(SVMul(Cross(expr.left.left, expr.right), expr.left.right))
            elif isinstance(expr.right, SVMul):
                return pull(SVMul(Cross(expr.left, expr.right.left), expr.right.right))
            else:
                if has_nested_scalars(expr):
                    return pull(Cross(pull(expr.left), pull(expr.right)))
                else:
                    return expr
        else:
            return expr

    elif isinstance(expr, MatrixExpr):
        if isinstance(expr, MAdd):
            return pull(expr.left) + pull(expr.right)

        elif isinstance(expr, MMMul):
            pass

        elif isinstance(expr, SMMul):
            pass

        else:
            return expr

    else:
        return expr


def simplify(expr):
    """
    Simplifies expr using standard operations (# TODO)
    :param expr:
    :return:
    """
    # expand
    simplify_expr = expand(expr)

    # pull
    simplify_expr = pull(simplify_expr)

    return simplify_expr
