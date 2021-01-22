"""
pydyn is python library for Dynamics on Manifolds.
"""

import sys

if sys.version_info < (3, 6):
    raise ImportError("Python version >= 3.6 is required")
del sys

from .data_types.scalars import Scalar, getScalars
from .data_types.vectors import Vector, getVectors
from .data_types.matrices import Matrix, SO3, getMatrices

from .operations.addition import Add, VAdd, MAdd
from .operations.multiplication import Mul, MMMul, MVMul, SMMul, SVMul, VVMul
from .operations.transpose import Transpose
from .operations.geometry import Delta, Dot, Cross, Hat, Vee

from .operations.dynamics import compute_eom
