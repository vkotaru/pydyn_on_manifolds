"""
PyDOM is python library for Dynamics on Manifolds. 
"""

from pydom.variables import vectors
import sys

if sys.version_info < (3, 6):
    raise ImportError("Python version >= 3.6 is required")
del sys

from . import variables
from . import operations
from .variables.variables import ScalarExpr, Expr, VectorExpr, MatrixExpr
from .variables.vectors import Vector
from .variables.scalars import Scalar