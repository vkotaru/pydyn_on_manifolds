class Test(object):
    def __init__(self):
        self.val = None

    def __dot__(self, other):
        print('performing dot operation')


x1 = Test()
x2 = Test()

y = x1.__dot__(x2)
