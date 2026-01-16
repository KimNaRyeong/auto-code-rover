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

def reproduce_issues():
    from sympy import Range, Symbol, oo
    errors = []

    # Issue 1: is_finite_set not implemented for Range
    try:
        finite_set_check = Range(5).is_finite_set
        if finite_set_check is None:
            raise AssertionError("is_finite_set property is not correctly implemented for Range.")
    except Exception as e:
        errors.append(e)

    # Issue 2: `sup` and `inf` don't work correctly for ranges with symbolic integers
    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    try:
        sup_result = s.sup
        raise AssertionError("Expected a ValueError for `sup` of a symbolic Range but none occurred.")
    except ValueError:
        pass  # This is the expected behavior; no action needed
    except Exception as e:
        errors.append(e)

    if errors:
        for error in errors:
            print_stacktrace(error)
        exit(1)  # Exit with 1 to indicate the presence of errors/issues
    else:
        print("No issues found, or the issues have been fixed. Exiting with code 0.")
        exit(0)

if __name__ == "__main__":
    reproduce_issues()
