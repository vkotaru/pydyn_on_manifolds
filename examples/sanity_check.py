from pydyn import *

a = Scalar('a')
b = Scalar('b')
sum_ab = a+b

v = Vector('v')
u = Vector('u')
x = Vector('x')
sum_uv = u+v

M = Matrix('M')
N = Matrix('N')
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


