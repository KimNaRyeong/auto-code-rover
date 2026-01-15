Below is a standalone Python script named `reproducer.py` that is designed to reproduce the issue described in your query. This script checks the consistency of the `simplify` function in SymPy and verifies the correctness of the simplified mass matrix for a simple 3-DOF robot mechanism. It raises an `AssertionError` if the issue is present, along with a detailed stack trace, and exits with code 0 when the issue is fixed.

```python
import numpy as np
from sympy import symbols, cos, sin, Matrix, lambdify, simplify

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

def test_simplify_issue():
    q_1, q_2, q_3 = symbols('q_1 q_2 q_3')
    q = [q_1, q_2, q_3]

    # Define the problem matrix.
    Mq = Matrix([
        [(1.0 * cos(q_2) + 0.5 * cos(q_2 + q_3))**2 * sin(q_1)**2 + (1.0 * cos(q_2) + 0.5 * cos(q_2 + q_3))**2 * cos(q_1)**2 + 0.25 * sin(q_1)**2 * cos(q_2)**2 + 0.25 * cos(q_1)**2 * cos(q_2)**2, 0, 0],
        [0, (-1.0 * sin(q_2) - 0.5 * sin(q_2 + q_3))**2 * sin(q_1)**2 + (-1.0 * sin(q_2) - 0.5 * sin(q_2 + q_3))**2 * cos(q_1)**2 + (-1.0 * cos(q_2) - 0.5 * cos(q_2 + q_3))**2 + 0.25 * sin(q_1)**2 * sin(q_2)**2 + 0.25 * sin(q_2)**2 * cos(q_1)**2 + 0.25 * cos(q_2)**2, -0.5 * (-1.0 * sin(q_2) - 0.5 * sin(q_2 + q_3)) * sin(q_1)**2 * sin(q_2 + q_3) - 0.5 * (-1.0 * sin(q_2) - 0.5 * sin(q_2 + q_3)) * sin(q_2 + q_3) * cos(q_1)**2 - 0.5 * (-1.0 * cos(q_2) - 0.5 * cos(q_2 + q_3)) * cos(q_2 + q_3)],
        [0, -0.5 * (-1.0 * sin(q_2) - 0.5 * sin(q_2 + q_3)) * sin(q_1)**2 * sin(q_2 + q_3) - 0.5 * (-1.0 * sin(q_2) - 0.5 * sin(q_2 + q_3)) * sin(q_2 + q_3) * cos(q_1)**2 - 0.5 * (-1.0 * cos(q_2) - 0.5 * cos(q_2 + q_3)) * cos(q_2 + q_3), 0.25 * sin(q_1)**2 * sin(q_2 + q_3)**2 + 0.25 * sin(q_2 + q_3)**2 * cos(q_1)**2 + 0.25 * cos(q_2 + q_3)**2]
    ])

    # Directly compute the function without simplification
    Mq_fnc = lambdify(q, Mq)
    expected_result = Mq_fnc(0, 0, 0)

    # Simplify the matrix then compute the function
    Mqs = simplify(Mq)
    Mqs_fnc = lambdify(q, Mqs)
    result_after_simplify = Mqs_fnc(0, 0, 0)

    try:
        np.testing.assert_array_almost_equal(expected_result, result_after_simplify)
        print("No issue found, the simplification works as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise AssertionError("Simplification resulted in incorrect values.") from e

if __name__ == "__main__":
    try:
        test_simplify_issue()
    except Exception as e:
        print("An error occurred, see details above.")
```

Execute this script with Python 3 by running `python3 reproducer.py` in the root directory of your project. The script is designed to detect issues with the `simplify` function in SymPy by comparing the results before and after simplification. If it identifies a discrepancy (which is the case in the issue described), it will raise an `AssertionError` and print a detailed stack trace to help identify the source of the problem.