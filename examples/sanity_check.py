from pydyn import *
from pydyn.utils.errors import ExpressionMismatchError

a, b, c = getScalars('a b c')
x, y, z = getVectors(['x', 'y', 'z'])
M, N = getMatrices('M N')

# Scalars
# -------
scalar_addition = a + b
scalar_scalar_scalar_add = a + b + c

try:
    scalar_vector_add = a + x
except ExpressionMismatchError:
    print('ExpressionMismatchError: scalar_vector_add = a + x')

scalar_scalar_mul = a * b
scalar_vector_mul = a * x
scalar_matrix_mul = a * M

# Vectors
# --------
vector_add = x + y
vec_vec_add = x + y + z

vec_scalar_mul = y * b
vec_vecT_mul = x * Transpose(y)
vecT_vec_mul = Transpose(x) * y
try:
    vec_vec_mul = x * y
except ExpressionMismatchError:
    print('ExpressionMismatchError: vec_vec_mul = x * y')

try:
    vec_mat_mul = x * M
except ExpressionMismatchError:
    print('ExpressionMismatchError: vec_mat_mul = x*M')
vecT_mat_mul = Transpose(x) * M

# Matrix
# ------
mat_add = M + N
mat_scalar_mul = N * b
mat_vec_mul = N * y
mat_mat_mul = M * N

# Mix and multiply
expr1 = M * (a + b)

# taking variation
# ----------------
scalar_sum_delta = scalar_addition.delta()
vector_sum_delta = vector_add.delta()
matrix_sum_delta = mat_add.delta()

scalar_prod_delta = scalar_scalar_mul.delta()
vec_scalar_mul_delta = vec_scalar_mul.delta()
vecT_vec_mul_delta = vecT_vec_mul.delta()
vec_vecT_mul_delta = vec_vecT_mul.delta()
mat_mat_mul_delta = mat_mat_mul.delta()
mat_vec_mul_delta = mat_vec_mul.delta()
mat_scalar_mul_delta = mat_scalar_mul.delta()

# print(R1R2)
print('done')
