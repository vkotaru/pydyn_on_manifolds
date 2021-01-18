from pydyn import Delta


def compute_eom(Lagrangian, inf_work, vars):
    """
    Computes Lagrange-Hamiltonian dynamics using principle of least action
    """

    # infinitesimal action
    dL = Lagrangian.delta()

    pass
