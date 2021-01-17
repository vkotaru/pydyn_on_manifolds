from pydyn.data_types.matrices import getMatrices
from pydyn.data_types.vectors import getVectors
from pydyn import *

a, b = getScalars('a b')
sum_ab = a+b

u, v, x = getVectors(['u', 'v', 'x'])
sum_uv = u+v

M, N = getMatrices('M N')
sum_MN = M+N

mul_ab = Mul(a,b)
mul_uv = MVMul(M,v)
mul_MN = MMMul(M,N)

R1 = Matrix('R1')
R2 = Matrix('R2')


expr = MVMul(SMMul(Add(a,b), M), VAdd(u, v))
# R1R2 = Mul(R1, R2)

# print(R1R2)
print('done')


