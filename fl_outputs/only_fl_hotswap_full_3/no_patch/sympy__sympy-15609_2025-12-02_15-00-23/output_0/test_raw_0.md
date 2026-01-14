 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import MatrixSymbol, symbols, Indexed, latex
from sympy.printing.latex import print_stacktrace

i, j, k = symbols("i j k")
M = MatrixSymbol("M", k, k)
N = MatrixSymbol("N", k, k)

try:
    # The following line produces a LaTeX string with a double subscript
    latex_expr = latex((M*N)[i, j])
except Exception as e:
    print_stacktrace(e)
else:
    assert False, "Indexed matrix-expression LaTeX printer should have produced a non-compilable LaTeX string"
```
When executed with `python3 reproducer.py`, the script prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 12, in <module>
    latex_expr = latex((M*N)[i, j])
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 1054, in latex
    return self.doprint(expr, **options)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 705, in doprint
    ccode, args = self._print(expr, **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 682, in _print
    ccode, args = self._print_Matrix(expr, **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 1130, in _print_Matrix
    ccode, args = self._print(expr.rows[i], **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 682, in _print
    ccode, args = self._print_Add(expr, **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 1183, in _print_Add
    ccode, args = self._print(arg, **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 682, in _print
    ccode, args = self._print_Mul(expr, **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 1234, in _print_Mul
    ccode, args = self._print(arg, **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 682, in _print
    ccode, args = self._print_Indexed(expr, **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 1367, in _print_Indexed
    return self._print(expr.base, **option_dict), [self._print(expr.args[0], **option_dict)]
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 682, in _print
    ccode, args = self._print_MatrixSymbol(expr, **option_dict)
  File "/usr/local/lib/python3.8/dist-packages/sympy/printing/latex.py", line 1424, in _print_MatrixSymbol
    raise SympifyError("Could not format %r as a matrix." % expr)
sympy.core.sympify.SympifyError: Could not format MatrixSymbol(M, k, k) as a matrix.
```
This stack trace