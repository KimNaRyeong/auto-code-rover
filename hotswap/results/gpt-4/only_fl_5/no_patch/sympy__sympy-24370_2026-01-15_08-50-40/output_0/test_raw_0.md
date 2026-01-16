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
    import sympy

    s0 = sympy.Symbol('s0')
    
    try:
        result = sympy.Integer(1024)//s0
        # As the division should not work as intended with the issue present, if it does, it means the issue is fixed.
        print("The issue seems to be fixed.")
    except TypeError as e:
        print_stacktrace(e)
        # Assert for the specific error message. If the message changes, this might need to be updated.
        assert "Argument of Integer should be of numeric type, got floor(1024/s0)." in str(e), "Unexpected error message"
        print("The issue is reproduced successfully.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "An unexpected error occurred."

if __name__ == "__main__":
    main()
```