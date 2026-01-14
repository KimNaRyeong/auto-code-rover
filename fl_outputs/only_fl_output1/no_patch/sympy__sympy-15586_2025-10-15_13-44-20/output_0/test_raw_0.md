```python
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

def main():
    import numpy as np
    from sympy import MatrixSymbol, lambdify
    
    try:
        X0 = MatrixSymbol('X0', 2, 2)
        xx = np.random.rand(4, 4)  # Original issue arises with a 4x4 float matrix

        # Inversion in numpy works but is not our focus
        np.linalg.inv(xx)

        # Inversion with sympy through lambdify
        X0Inv = X0**-1
        symInv = lambdify(X0, X0Inv)
        result = symInv(xx)  # The line expected to raise an error if issue is present

        # If the process reaches this line without an error, the issue is presumed fixed
        print("No issue detected.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is reproducible.")

if __name__ == "__main__":
    main()
```

This script is designed to be a standalone python file named `reproducer.py` which will try to reproduce the mentioned issue. Upon running, it will execute the problematic code. If the issue is present, it will catch the exception, print the stack trace of the error using the provided `print_stacktrace` function, and raise an `AssertionError`. If no error occurs (indicating the issue is fixed or not present in the environment the script was run in), it prints "No issue detected." and exits with code 0.