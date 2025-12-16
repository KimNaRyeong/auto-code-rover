import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ZeroMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def as_explicit(self):
        return [[0]*self.cols for _ in range(self.rows)]

    def __nonzero__(self):
        return True

def main():
    Z = ZeroMatrix(2, 3)
    Ze = Z.as_explicit()

    print(Z)
    print(Ze)
    print(bool(Z))
    print(bool(Ze))

    try:
        assert bool(Z) == False
    except AssertionError:
        print_stacktrace(AssertionError("ZeroMatrix should not be falsey"))
        sys.exit(1)

if __name__ == "__main__":
    main()
