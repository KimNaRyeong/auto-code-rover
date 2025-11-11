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

try:
    assert 2 // 0.5 == 4, "Expected 4"
    S = type('S', (), {'Half': classmethod(lambda cls: 0)})
    assert S.Half() != 0, "Expected non-zero value for S.Half()"
    assert S(2) // S.Half() != 4, "Expected ZeroDivisionError"
except ZeroDivisionError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue is fixed")
    exit(0)
