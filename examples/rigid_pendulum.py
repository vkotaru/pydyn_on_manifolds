from pydyn import *
from pydyn.operations.print_tree import print_latex
from pydyn.utils.errors import ExpressionMismatchError
import numpy as np


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
    rigid_pendulum()
