from numpy.lib.utils import get_include
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name="IsingRutinas",
    ext_modules=cythonize("IsingRutinas.pyx", annotate=True),
    include_dirs=[numpy.get_include()],
    zip_safe=False
)
