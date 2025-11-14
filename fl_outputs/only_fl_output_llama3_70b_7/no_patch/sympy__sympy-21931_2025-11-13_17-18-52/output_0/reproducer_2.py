import sympy.combinatorics as comb

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

def test_partition_printing():
    p = comb.Partition([1, 2])
    expected_str = "Partition({1, 2})"
    actual_str = str(p)
    if actual_str != expected_str:
        raise AssertionError(f"Expected {expected_str}, got {actual_str}")

try:
    test_partition_printing()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
