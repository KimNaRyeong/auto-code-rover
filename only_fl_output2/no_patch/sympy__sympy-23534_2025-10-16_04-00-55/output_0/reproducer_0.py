# reproducer.py

import sympy as smp

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
    try:
        # Create symbol-like objects using `symbols` with an extra layer of parentheses
        q, u = smp.symbols(('q:2', 'u:2'), cls=smp.Function)
        
        # Check if the type of q[0] is as expected
        assert isinstance(q[0], smp.FunctionClass), "q[0] is not an instance of UndefinedFunction"
        
    except AssertionError as e:
        print_stacktrace(e)
        raise

    print("No issues detected.")

if __name__ == "__main__":
    main()
