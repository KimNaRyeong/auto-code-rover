import sty

def test_import():
    from sty import fg  # This line should raise a KeyError: '__wrapped__'

try:
    test_import()
except KeyError as e:
    if "'__wrapped__'" in str(e):
        print_stacktrace(e)
        assert True, "KeyError: '__wrapped__' is expected"
    else:
        print("Unexpected error:", e)
        assert False, "Unexpected error"
except Exception as e:
    print("Unexpected error:", e)
    assert False, "Unexpected error"
else:
    print("No error raised. The issue is fixed.")
    assert False, "The issue should be present"

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

test_import()
