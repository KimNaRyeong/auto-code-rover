import sys
import traceback
from sympy import Matrix

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Arrange
    M1 = Matrix.zeros(0, 0)
    M2 = Matrix.zeros(0, 1)
    M3 = Matrix.zeros(0, 2)
    M4 = Matrix.zeros(0, 3)

    # Act
    hstacked_matrix_1 = Matrix.hstack(M1, M2, M3, M4)
    hstacked_matrix_2 = Matrix.hstack(M1, M2, M3)

    # Assert
    expected_shape_1 = (0, 6)
    actual_shape_1 = hstacked_matrix_1.shape
    assert expected_shape_1 == actual_shape_1, f"Expected shape {expected_shape_1} but got {actual_shape_1}"

    expected_shape_2 = (0, 3)
    actual_shape_2 = hstacked_matrix_2.shape
    assert expected_shape_2 == actual_shape_2, f"Expected shape {expected_shape_2} but got {actual_shape_2}"

    vstacked_matrix = Matrix.vstack(hstacked_matrix_1, hstacked_matrix_2)
    expected_shape_3 = (2, 3)
    actual_shape_3 = vstacked_matrix.shape
    assert expected_shape_3 == actual_shape_3, f"Expected shape {expected_shape_3} but got {actual_shape_3}"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
