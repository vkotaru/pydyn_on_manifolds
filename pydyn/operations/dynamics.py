from pydyn import Delta
from pydyn.operations.integration import integrate_by_parts_vectors
from pydyn.operations.simplification import full_simplify


def compute_eom(Lagrangian, inf_work, vars):
    """
    Computes Lagrange-Hamiltonian dynamics using principle of least action
    """

    # taking variation of lagrangian
    dL = Lagrangian.delta()
    # infinitesimal action integral
    dS = dL + inf_work
    dS = full_simplify(dS)

    # integration by parts
    vector_dots = []
    for v in vars[1]:
        vector_dots.append(v.variation_vector().diff())

    dS = integrate_by_parts_vectors(dS, vector_dots)

    print('eom done')
