
class ExpressionMismatchError(Exception):
    """Expression mismatch during the operation"""
    def __init__(self):
        # TODO add operation and message types
        msg = "this operation cannot be performed between two different data_types"
        super().__init__(msg)

