from sympy import *
import traceback, sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def bool_map_test():
    A1, A2 = symbols('A1, A2')
    f1 = Xor(A1, A2)
    f2 = ~(Xor(A1, A2))
    bool_map_f1_f2 = bool_map(f1, f2)
    bool_map_f2_f1 = bool_map(f2, f1)
    assert bool_map_f1_f2 == bool_map_f2_f1, "bool_map returned different results for f1 and f2"

if __name__ == "__main__":
    try:
        bool_map_test()
        print("No issue found.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
