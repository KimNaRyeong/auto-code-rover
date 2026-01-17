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

def main():
    from sympy import Function, solve
    
    # Define an arbitrary function f
    f = Function('f')
    
    # Check if the function application with a numeric argument is considered a number
    try:
        assert not f(1).is_number, "Undefined functions with number arguments should have is_number be False."
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # Further, check if solve behaves as expected when applied to such a case
    try:
        solution = solve(f(1) - 2, f(1))
        expected_solution = []  # Assuming the correct behavior should not yield a direct numerical solution
        assert solution == expected_solution, "solve(f(1) - 2, f(1)) should not yield a direct numerical solution."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
