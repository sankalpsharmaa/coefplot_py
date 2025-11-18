"""
coefplot_py - Python implementation of Stata's coefplot

This package provides a Python implementation of Stata's coefplot functionality
that can be called directly from Stata (Stata 16+) or used standalone in Python.

Main components:
- tools.py: Core plotting functionality
- coefplot_py.ado: Stata wrapper command
"""

__version__ = "1.0.0"

# Import main functions for easy access (re-export)
try:
    from .tools import coefplot_py, CoefPlot, coefplot_from_stata  # noqa: F401
    __all__ = ['coefplot_py', 'CoefPlot', 'coefplot_from_stata']
except ImportError:
    # If tools.py is not available, provide empty __all__
    __all__ = []
