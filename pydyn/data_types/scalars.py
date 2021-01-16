from pydyn.operations.addition import Add, VAdd, MAdd

class Scalar(object):
    def __init__(self, s=None, value=None, attr=None):
        self.name = s
        self.size = (1,)
        self.value = value
        self.type = 'ScalarExpr'

        self.attr = attr
        if (self.attr == 'Constant'):
            self.isConstant = True
        else:
            self.isConstant = False

    def __str__(self):
        return self.name

    def __add__(self, other):
        if other.type=='ScalarExpr':
            return  Add(self, other)
        else:
            from pydyn.utils.errors import ExpressionMismatchError
            raise ExpressionMismatchError

    #  # def delta(self):  #     if self.isConstant:  #         return Scalar('0', value=0)  #     else:  #         name = 'delta{'+self.name+'}'  #         delta_cls = Delta(Scalar(name, value=self.value))  #         return delta_cls
