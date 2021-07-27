from pydyn import *
from pydyn.operations.addition import Add, VAdd, MAdd
from pydyn.base.scalars import getScalars

add = Add()
a, b, c, d, e = getScalars('a b c d e')
f, g = getScalars('f g', attr=['Constant'])

sum_scalars = Add(a, b, Add(c, d, e), [f, g])
delta_sum_scalars = sum_scalars.delta()
dot_sum_scalars = sum_scalars.diff()
dot_sum2_ = Add(f, g).diff()
scalar_scalar_mul = a * sum_scalars
sum_scalars2 = sum_scalars.copy()
sum_scalars2.replace_at(0, e)

v, u = getVectors('u v', attr=['Constant'])
x, y, z = getVectors(['x', 'y', 'z'])
sum_vectors = VAdd(u, v)
sum_vectors += VAdd(x, y, z)

A, B, C = getMatrices('A B C')
sum_matrices = A + MAdd(B, C)
dot_sum_matrices = sum_matrices.diff()

print('done')
