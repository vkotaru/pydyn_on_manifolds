
class ExpressionMismatchError(Exception):
    """Expression mismatch during the operation"""
    def __init__(self, operation='', ltype='', rtype='' ):
        msg =  operation + 'cannot be performed between ' + ltype + ' and ' + rtype
        super().__init__(msg)

class UndefinedCaseError(Exception):
    """New case found"""
    def __init__(self ):
        # TODO add operation and message types
        msg =  'New (undefined) case has been found'
        super().__init__(msg)