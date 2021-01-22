from pydyn import *
from pydyn.operations.print_tree import print_latex
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

    eqs = compute_eom(L, deltaW, [[], [x], []])
    print_latex(eqs)

    print('done')


def rigid_pendulum():
    J = Matrix('J', attr=['Constant', 'SymmetricMatrix'])
    rho = Vector('rho', attr=['Constant'])
    m, g = getScalars('m g', attr=['Constant'])
    e3 = Vector('e3', attr=['Constant'], value=np.array([0., 0., 1]))

    M = Vector('M')
    R = SO3('R')
    Om = R.get_tangent_vector()
    eta = R.get_variation_vector()

    KE = Dot(Om, J * Om) * 0.5
    PE = m * g * Dot(R * rho, e3)
    L = KE-PE

    deltaW = Dot(eta, M)
    eqns = compute_eom(L, deltaW, [[],[],[R]])

    print('done')


if __name__ == "__main__":
    # point_mass()
    rigid_pendulum()
