# reproducer.py
import sys
from sympy.matrices import randMatrix

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    # Generate a 3x3 symmetric matrix with 1 percent non-zero elements
    m1 = randMatrix(3, symmetric=True, percent=1)
    # Generate a 3x3 symmetric matrix with 50 percent non-zero elements
    m2 = randMatrix(3, symmetric=True, percent=50)
    # Generate a 3x3 symmetric matrix with 99 percent non-zero elements
    m3 = randMatrix(3, symmetric=True, percent=99)
    # Generate a 3x3 symmetric matrix with 0 percent non-zero elements
    m4 = randMatrix(3, symmetric=True, percent=0)
    
    # Check if matrices m1, m2, m3, and m4 are symmetric
    assert m1 == m1.transpose(), "Matrix with 1 percent non-zero elements is not symmetric"
    assert m2 == m2.transpose(), "Matrix with 50 percent non-zero elements is not symmetric"
    assert m3 == m3.transpose(), "Matrix with 99 percent non-zero elements is not symmetric"
    assert m4 == m4.transpose(), "Matrix with 0 percent non-zero elements is not symmetric"
    
    print("Success: All generated matrices are symmetric.")

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with non-zero status to indicate failure

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)  # General error

sys.exit(0)  # Exit with zero to indicate success
