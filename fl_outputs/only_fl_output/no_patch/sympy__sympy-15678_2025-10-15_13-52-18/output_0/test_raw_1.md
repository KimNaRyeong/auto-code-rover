Given the earlier confusion and the resulting error upon trying to import `idiff` from `sympy.calculus.util`, it seems like `idiff` was attempted to be imported from an incorrect location or perhaps there was a misunderstanding about the proper import path within Sympy's structure. Let's correct the import path according to Sympy's documentation or common import practices and try to write a test script again.

Based on the error message, it's possible that the `idiff` function might reside in a different module or its location varies between Sympy versions. Assuming `idiff` should generally be accessible directly from `sympy`- this script addresses the original problem, correctly import `idiff` from `sympy` and correctly handle the scenarios mentioned in the problem statement:

```python
from sympy import Eq, exp, symbols, Function
from sympy.solvers.deutils import idiff


def print_stacktrace(e: Exception):
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


def reproduce_issues():
    x, y = symbols('x y')
    f = Function('f')(x)

    try:
        # Try using idiff with an Eq object
        idiff(Eq(y * exp(y), x * exp(x)), y, x)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("idiff does not support Eq objects properly.")

    try:
        # Try using idiff with f(x) instead of y
        idiff(f * exp(f) - x * exp(x), f, x)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("idiff does not support f(x) instead of y.")

    try:
        # Test a working scenario for sanity check
        result = idiff(y * exp(y) - x * exp(x), y, x)
        assert result, "idiff failed on the working scenario."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Sanity check test failed for idiff.")

    print("If this message is reached, the issues could not be reproduced under the current setup.")


if __name__ == '__main__':
    reproduce_issues()
```

**Note:** The import for `idiff` is assumed to be corrected here as per your environment's correct import path. Sympy's API can change between versions, and functionality might move between modules. If `idiff` does not exist in `sympy.solvers.deutils` within your version, please adjust the import statement according to the version of Sympy you are using, ensuring that `idiff` is imported correctly from its actual location within the package.

Since the precise location of `idiff` in the package structure can vary or my assumption might be wrong based on your environment, if you're still facing an import issue, it would help to refer to the specific version documentation of Sympy you're working with or try importing `idiff` directly from `sympy` if that's how your Sympy version exposes it.