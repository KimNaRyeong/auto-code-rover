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
    @staticmethod
    def Half():
        return 0.5

try:
    assert 2 // 0.5 == 4, "Expected 4"
    s = S()
    result = s.Half()
    assert 2 // result != 4, "Issue is fixed"
    raise AssertionError("Issue is present")
except ZeroDivisionError as e:
    print_stacktrace(e)
    raise
