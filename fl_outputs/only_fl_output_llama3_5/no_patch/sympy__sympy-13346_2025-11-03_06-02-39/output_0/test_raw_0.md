Here is the reproducer script:

```python
import numpy as np
from sympy import *
from test_sums_products import test_evalf_fast_series, test_evalf_fast_series_issue_4021
from test_quadrature import test_legendre, test_laguerre, test_laguerre_precise, test_hermite, test_gen_laguerre, test_gen_laguerre_precise, test_jacobi, test_jacobi_precise
from test_rootoftools import test_CRootOf_eval_rational
from test_lambdify import test_sin
from matrices.matrices import DeferredVector

def main():
    try:
        test_evalf_fast_series()
        test_evalf_fast_series_issue_4021()
        test_legendre()
        test_laguerre()
        test_laguerre_precise()
        test_hermite()
        test_gen_laguerre()
        test_gen_laguerre_precise()
        test_jacobi()
        test_jacobi_precise()
        test_CRootOf_eval_rational()
        test_sin()
        DeferredVector(func=lambda x: x**2, symbols='x')
    except AssertionError as e:
        print_stacktrace(e)
        raise

def print_stacktrace(e):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

This script will run the failing tests and raise an `AssertionError` if any of them fail. The stack trace of the error will be printed using the provided function.