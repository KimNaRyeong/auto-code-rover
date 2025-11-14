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

try:
    p1 = comb.Partition([1,2])
    assert str(p1) != "Partition(FiniteSet(1, 2))", f"Expected a nicer printing of Partition, got {str(p1)}"
    
    p2 = comb.Partition({1,2})
    assert str(p2) != "Partition(FiniteSet(1, 2))", f"Expected a nicer printing of Partition, got {str(p2)}"
    
    print("Issue not present. Exiting with code 0.")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
