"""
PyDOM is python library for Dynamics on Manifolds. 
"""

from pydom.variables import vectors
import sys

if sys.version_info < (3, 6):
    raise ImportError("Python version >= 3.6 is required")
del sys

from . import variables, operations, utils 
from .variables.variables import Expr, ScalarExpr, VectorExpr, MatrixExpr
from .variables.scalars import Scalar
from .variables.vectors import Vector
from .variables.matrices import Matrix

from .operations.multiple import Mul
from .operations.add import Add