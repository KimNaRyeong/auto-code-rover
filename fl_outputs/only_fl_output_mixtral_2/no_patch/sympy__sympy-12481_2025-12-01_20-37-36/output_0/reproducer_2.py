import sys

class Permutation:
    def __init__(self, cycles):
        self.cycles = sorted(cycles, key=lambda c: c[0])
        self.permutation = [0] * len(cycles)
        for i, cycle in enumerate(self.cycles):
            for j in cycle:
                self.permutation[j] = i

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    Permutation([[0, 1], [0, 1]])
    assert False, "ValueError should have been raised"
except ValueError as e:
    pass
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
