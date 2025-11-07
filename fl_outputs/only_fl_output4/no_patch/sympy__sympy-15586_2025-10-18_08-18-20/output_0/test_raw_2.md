Based on the request to reproduce the issue described and print a stack trace if an error occurs, I have crafted a Python script titled `reproducer.py`. This script attempts to replicate the core issue where the use of `lambdify` in `sympy` on a NumPy matrix fails due to a `TypeError`. If the issue is successfully reproduced (i.e., the `TypeError` is caught), it will print a detailed stack trace incorporating the aforementioned function. Conversely, if the operation succeeds (indicating a fix), the script exits with code 0, signalling resolution.

Here is the tailored script:

```python
# reproducer.py

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

try:
    import numpy as np
    from sympy import MatrixSymbol, lambdify, init_printing
    
    init_printing()

    X0 = MatrixSymbol('X0', 2, 2)
    xx = np.random.rand(4, 4)  # This creates a float matrix that earlier caused the issue
    X0Inv = X0**-1
    np.linalg.inv(xx)  # Testing if NumPy can invert the float matrix without issues
    
    symInv = lambdify(X0, X0Inv, 'numpy')  # Explicitly setting module to numpy
    result = symInv(xx)  # This line should cause the TypeError as described in the issue
    assert False, "The expected error did not occur."  # Force an assertion if the above line doesn't fail

except AssertionError as e:
    print("AssertionError indicating either a successful run or another issue occurred.")
    print_stacktrace(e)
    sys.exit(1)  # Use an exit code to indicate an unsuccessful reproduction if the error didn't match expectations

except Exception as e:
    print_stacktrace(e)  # This will print the stack trace for the specific TypeError described
    sys.exit(1)  # Exiting with a non-zero code to indicate an error occurred, which in this context is expected

print("Success: The issue has been resolved.")
sys.exit(0)  # Indicate the issue is fixed by exiting with code 0
```

### How to Use:

1. Ensure `numpy` and `sympy` are installed in your environment. You can install these packages using pip:
   ```bash
   pip install numpy sympy
   ```
2. Save the above script as `reproducer.py` in the root directory of your project.
3. Run the script using Python 3:
   ```bash
   python3 reproducer.py
   ```
4. Observe the output:
   - If the script exits with code `0`, this suggests the issue has been resolved.
   - If the script prints a stack trace and exits with code `1`, it indicates the script successfully reproduced the TypeError issue as originally reported.