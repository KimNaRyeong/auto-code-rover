```python
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

def check_is_finite_set_implementation():
    from sympy import Range
    try:
        assert hasattr(Range(5), 'is_finite_set'), "is_finite_set property not implemented for Range"
    except AssertionError as e:
        print("Issue with is_finite_set property missing for Range detected.")
        raise e

def check_sup_inf_error():
    from sympy import symbols, oo, Range
    n = symbols('n', integer=True)
    s = Range(n, oo, 1)
    try:
        sup_exception = False
        try:
            _ = s.sup
        except Exception as e:
            sup_exception = True
            print("Issue with 'sup' for Range with symbolic integers detected.")
            print_stacktrace(e)
        
        assert sup_exception, "No exception for 'sup' on Range with symbolic integer, but issue expected."
    except AssertionError as e:
        raise e

if __name__ == "__main__":
    try:
        check_is_finite_set_implementation()
        check_sup_inf_error()
    except AssertionError as main_exception:
        print_stacktrace(main_exception)
        exit(1)  # Exit with a non-zero code to indicate an issue is present
    print("All checks passed successfully.")
    exit(0)  # Exit with 0 to indicate no issues
```