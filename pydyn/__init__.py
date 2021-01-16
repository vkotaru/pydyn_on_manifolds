"""
pydyn is python library for Dynamics on Manifolds.
"""

import sys

if sys.version_info < (3, 6):
    raise ImportError("Python version >= 3.6 is required")
del sys

# from . import data_types, operations, utils
from .data_types.scalars import Scalar
from .data_types.vectors import Vector
from .data_types.matrices import Matrix

# from .operations.multiple import Mul
from .operations.addition import Add, VAdd, MAdd
from .operations.multiplication import Mul, MMMul, MVMul, SMMul, SVMul, VVMul