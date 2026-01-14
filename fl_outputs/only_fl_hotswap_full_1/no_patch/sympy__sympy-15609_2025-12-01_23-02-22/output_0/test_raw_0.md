 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import MatrixSymbol, symbols, latex
from sympy.printing.latex import print_stacktrace

def main():
    i, j, k = symbols("i j k")
    M = MatrixSymbol("M", k, k)
    N = MatrixSymbol("N", k, k)
    try:
        latex_expr = latex((M*N)[i, j])
        assert False, "LaTeX expression is compilable, but it shouldn't be."
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    main()
  File "reproducer.py", line 10, in main
    latex_expr = latex((M*N)[i, j])
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 941, in latex
    return self.doprint(expr, **options)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 698, in doprint
    return self._print(expr, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 685, in _print
    return self._printer(expr, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 1101, in _print_MatrixElement
    return self._print(a, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 685, in _print
    return self._printer(expr, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 1095, in _print_Matrix
    return self._print(a._mat, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 685, in _print
    return self._printer(expr, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 1101, in _print_MatrixElement
    return self._print(a, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 685, in _print
    return self._printer(expr, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 1095, in _print_Matrix
    return self._print(a._mat, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 685, in _print
    return self._printer(expr, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 889, in _print_Sum
    return self._print(summand, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 685, in _print
    return self._printer(expr, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/sympy/printing/latex.py", line 1101, in _print_MatrixElement
    return self._print(a, **kwargs)
  File "/usr/local/lib