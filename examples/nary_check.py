from pydyn import *
from pydyn.operations.addition import Add, VAdd, MAdd
from pydyn.base.scalars import getScalars

add = Add()
a, b, c, d, e = getScalars('a b c d e')
f, g = getScalars('f g', attr=['Constant'])

sumS = Add(a, b, Add(c, d, e), [f, g], 0, 9)
delta_sumS = sumS.delta()
dot_sumS = sumS.diff()
dot_sum2_ = Add(f, g).diff()
scalar_scalar_mul = a * sumS
sumS2 = sumS + 2
sumS2.replace_at(0, e)

v, u = getVectors('u v', attr=['Constant'])
x, y, z = getVectors(['x', 'y', 'z'])
sumV = VAdd(u, v)
sumV += VAdd(x, y, z)

A, B, C = getMatrices('A B C')
sumM = A + MAdd(B, C)
dot_sumM = sumM.diff()

###########################
mulS = Mul(a, b, Mul(c, d), [e, f], 2, 5)
mulS2 = mulS.copy()
del_mulS = mulS.delta()
dot_mulS = mulS.diff()

print('done')
