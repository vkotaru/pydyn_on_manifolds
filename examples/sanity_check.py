from pydom import *

class Test(object):
    def __init__(self):
        self.x = 0


R1 = Matrix('R1')
R2 = Matrix('R2')

R1R2 = Mul(R1, R2)

print(R1R2)
print('done')


