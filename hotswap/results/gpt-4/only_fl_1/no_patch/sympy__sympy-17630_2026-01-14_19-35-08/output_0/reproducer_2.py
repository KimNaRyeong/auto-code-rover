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
    from sympy import MatrixSymbol, ZeroMatrix, BlockMatrix, block_collapse
    a = MatrixSymbol("a", 2, 2)
    z = ZeroMatrix(2, 2)
    b = BlockMatrix([[a, z], [z, z]])

    try:
        # Attempt to perform block multiplication that previously caused an exception
        result = block_collapse(b * b * b)

        # If no exception occurs, we assert False as the script should only complete without error if the issue is fixed
        assert False, "No exception raised, the issue may have been fixed."

    except AttributeError as e:
        # Here we catch the specific expected AttributeError to confirm the issue,
        # then print the stack trace for debugging purposes
        if "'Zero' object has no attribute 'cols'" in str(e):
            print_stacktrace(e)
            exit(0)  # Exit with code 0 to indicate script executed as expected for the current issue state
        else:
            # If another AttributeError occurred, rethrow it to avoid masking different errors.
            raise
    except Exception as e:
        # This catches all other exceptions to prevent the script from failing silently
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate an unexpected error occurred

if __name__ == "__main__":
    main()
