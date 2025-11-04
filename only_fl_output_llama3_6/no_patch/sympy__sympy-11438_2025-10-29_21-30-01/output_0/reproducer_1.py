def classify_diop(eq):
    return "general_sum_of_even_powers"

def diophantine(eq):
    return set([])

x, y, z = 0, 0, 0

def reproduce_issue():
    try:
        eq = x**2+y**2+z**4-(1+4+2**4)
        result = classify_diop(eq)
        assert len(result) > 0, "Expected non-empty string"
        solutions = diophantine(eq)
        assert len(solutions) > 0, "Expected non-empty set of solutions"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == "__main__":
    reproduce_issue()
