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

class S:
    Half = 0.5

try:
    assert 2 // 0.5 == 4, "Expected 4"
    result = S(2) // S.Half
    assert result != 0, "Expected non-zero value, got ZeroDivisionError"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
