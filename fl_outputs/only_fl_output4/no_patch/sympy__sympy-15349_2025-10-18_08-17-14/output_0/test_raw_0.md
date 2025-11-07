Here's a Python script named `reproducer.py` that matches your criteria. Place this script in the root directory of the project and run it using `python3 reproducer.py`. It checks the output of `Quaternion.to_rotation_matrix()` for correctness, raising an `AssertionError` with a stack trace if the issue is detected, and exits with code 0 if the issue is fixed.

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

def test_quaternion_to_rotation_matrix():
    import sympy
    from sympy import symbols, cos, sin, Quaternion, trigsimp

    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    rotation_matrix = trigsimp(q.to_rotation_matrix())

    # Expecting one of the sin(x) to be negative for correct rotation matrix
    expected_matrix = sympy.Matrix([
        [1,       0,        0],
        [0,  cos(x), -sin(x)],
        [0,  sin(x),  cos(x)]
    ])

    assert rotation_matrix == expected_matrix, "Quaternion.to_rotation_matrix() output is incorrect."

if __name__ == '__main__':
    try:
        test_quaternion_to_rotation_matrix()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    print("Test passed. The issue is fixed.")
    exit(0)
```

This script not only attempts to reproduce the reported issue but also ensures that if any exception is raised during the process, it gives clear feedback through a printed stack trace. Additionally, it respects your request for exiting with code 0 if the issue is fixed or providing detailed diagnostics in case of failure or error.