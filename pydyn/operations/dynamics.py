from pydyn import Delta
from pydyn.operations.simplification import simplify


def compute_eom(Lagrangian, inf_work, vars):
    """
    Computes Lagrange-Hamiltonian dynamics using principle of least action
    """
    # Step: 0
    # format the tree in to desired format
    # ------------------------------------

    # Step:1
    # ------
    # taking variation of lagrangian
    dL = Lagrangian.delta()
    # infinitesimal action integral
    dS = dL + inf_work
    dS = simplify(dS)

    print('eom done')
