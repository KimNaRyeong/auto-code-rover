def reproducer():
    s = 'test_boo[..'  # simulate the problematic headline
    modified_s = s.replace(".[", "[")  # this line causes the problem
    assert modified_s == 'test_boo[..['  # this assertion should fail due to the bug

if __name__ == '__main__':
    try:
        reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        raise SystemExit(0)

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
