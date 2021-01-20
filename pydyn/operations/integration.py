from pydyn.operations.expansion import expand
from pydyn.operations.simplification import full_simplify


def integrate_by_parts_vectors(expr, vectors):
    expr = expand(expr)
    expr = full_simplify(expr)
    for vector in vectors:
        # expr = col(expr, vector)
        # expr = ibp(expr, vector)
        expr = full_simplify(expr)

    return expr


def integrate_by_parts_scalars(expr, scalars):
    expr = expand(expr)
    expr = full_simplify(expr)
