import sys

class Permutation:
    def __init__(self, cycles):
        self.cycles = [tuple(sorted(cycle)) for cycle in cycles]
        self.size = max(max(cycle) for cycle in self.cycles) + 1
        self.permutation = [0] * self.size
        for cycle in self.cycles:
            for i in range(len(cycle) - 1):
                self.permutation[cycle[i]] = cycle[i + 1]
            self.permutation[cycle[-1]] = cycle[0]
        self.inverse = [0] * self.size
        for i in range(self.size):
            self.inverse[self.permutation[i]] = i

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        Permutation([[0, 1], [0, 1]])
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("ValueError should not be raised")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Another exception should not be raised")
    else:
        print("No exception was raised, which is unexpected.")
        raise AssertionError("No exception was raised, which is unexpected.")
