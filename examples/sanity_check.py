from pydom.operations.add import Add
from pydom.variables.scalars import Scalar
from pydom import *
import pydom 

class Test(object):
    def __init__(self):
        self.x = 0

x = Vector('x', size=3)

z = Scalar('z')
dz = z.delta()

m = Scalar('m', attr='Constant')
dm = m.delta()

Add(m,z)

x = Vector('x', attr='Constant')
dx = x.delta()

print(dx)
print('done')


