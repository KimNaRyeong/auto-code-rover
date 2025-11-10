def floor(x):
    if x >= 0:
        return int(x)
    else:
        return -int(-x)

def ceiling(x):
    if x >= 0:
        return int(x) + 1
    else:
        return -int(-x)

assert not (floor(-1) < 0 and floor(1) >= 0 and ceiling(-1) <= 0)
try:
    raise AssertionError("Issue not reproduced")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue fixed!")
    exit(0)

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

