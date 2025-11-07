from sympy.combinatorics import Partition

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
    p1 = Partition([1,2])
    p2 = Partition({1,2})
    
    assert str(p1) == "Partition({1, 2})", f"Expected 'Partition({1, 2})', got '{str(p1)}'"
    assert str(p2) == "Partition({1, 2})", f"Expected 'Partition({1, 2})', got '{str(p2)}'"

try:
    test_partition_printing()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
