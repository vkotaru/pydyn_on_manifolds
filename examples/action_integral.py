from pydyn import *
from pydyn.utils.errors import ExpressionMismatchError
import numpy as np


def point_mass():
    """
    Derives Newton's equation of motion for 3d point mass

    Variables
    scalars: mass: m [kg]
             gravity: g [m/s^2]

    vectors: neg gravity direction: e3 [0,0,1] [No units]
             point-mass position: x  [m]
             input force: f [N]

    :return: None
    """
    m, g = getScalars('m g', attr=['Constant'])
    e3 = Vector('e3', attr=['Constant'], value=np.array([0., 0., 1]))
    x, f = getVectors(['x', 'f'])

    v = x.diff()

    # computing energies
    PE = m * x.dot(g * e3)
    KE = m * Dot(v, v) * 0.5

    # Lagrangian
    L = KE - PE

    # infinitesimal work
    deltaW = Dot(x.delta(), f)

    compute_eom(L, deltaW, [x])

    pass


if __name__ == "__main__":
    point_mass()
