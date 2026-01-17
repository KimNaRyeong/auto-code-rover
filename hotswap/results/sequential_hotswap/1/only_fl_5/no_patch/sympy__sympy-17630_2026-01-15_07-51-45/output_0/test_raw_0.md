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

def test_block_matrix_multiplication():
    from sympy import MatrixSymbol, ZeroMatrix, BlockMatrix, block_collapse
    
    a = MatrixSymbol("a", 2, 2)
    z = ZeroMatrix(2, 2)
    b = BlockMatrix([[a, z], [z, z]])
    
    # First block-multiplication should work fine
    try:
        result = block_collapse(b * b)
        assert result.shape == (4, 4), "The shape of the result matrix is incorrect"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("First block-multiplication failed") from e

    # Second block-multiplication should also work but likely raises an exception
    try:
        result = block_collapse(b * b * b)
        assert result.shape == (4, 4), "The shape of the result matrix is incorrect"
        # If no exception is raised, the bug is fixed and we exit with code 0
        print("Issue fixed.")
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("Exception occurred during second block-multiplication")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_block_matrix_multiplication()
    except AssertionError as e:
        # Only catch assertion errors to avoid exiting with code 0 for unexpected exceptions
        print(e)
        exit(1)
    exit(0)
```

This script tests for the specific issue where performing block-multiplication on a `BlockMatrix` containing `ZeroMatrix` blocks multiple times causes an exception due to a `Zero` object lacking an expected attribute. The `print_stacktrace` function is used to print detailed traceback information if an exception is caught during the test execution. The script ensures an `AssertionError` is raised when the issue is present, providing a detailed stack trace for debugging purposes. Conversely, it will exit with code 0 when the issue is resolved, indicating the absence of the problem.
