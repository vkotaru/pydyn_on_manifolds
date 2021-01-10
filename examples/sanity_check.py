from pydom.variables.scalars import Scalar
from pydom import *
import pydom 

x = Vector('x', size=3)

z = Scalar('z')
dz = z.delta()

print(dz)
print('done')


