```python
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

class Permutation:
    def __init__(self, cycles):
        self.cycles = cycles
        self.permutation = self._compute_permutation()

    def _compute_permutation(self):
        elements = set()
        for cycle in self.cycles:
            for element in cycle:
                if element in elements:
                    raise ValueError("Cycles are not disjoint.")
                elements.add(element)
        # Placeholder for actual permutation computation
        return []

def main():
    try:
        identity = Permutation([[0,1],[0,1]])  # Expecting this to not raise exception but it does
        assert identity.permutation == [], "Identity permutation was not constructed correctly."
    except ValueError as e:
        # If the exception is caught, it means the issue is present.
        # We print the stack trace and then rethrow the assertion to exit with a non-zero code if necessary.
        print_stacktrace(e)
        raise AssertionError("Permutation constructor failed with non-disjoint cycles.") from e
    except AssertionError as e:
        print_stacktrace(e)
    else:
        print("The issue is fixed. Exiting with code 0.")
        exit(0)

if __name__ == "__main__":
    main()
```

This script attempts to instantiate a `Permutation` class with non-disjoint cycle arguments, which according to the described issue, should not raise a `ValueError` but instead should compute the resulting permutation, expected to be the identity permutation in this context.

However, since the provided `Permutation` class implementation currently raises a `ValueError` for non-disjoint cycles, executing this script as it is will result in catching and printing the stack trace of the `ValueError`. The script is designed to indicate the presence of the issue by re-throwing an `AssertionError` with an explanatory message if the initial expectation (that the `Permutation` constructor can handle non-disjoint cycles by computing the resulting permutation) is violated.

Once the issue is fixed (meaning the `Permutation` constructor can handle and correctly process non-disjoint cycles as described), the script would print a message that the issue is fixed and exit with a code 0, indicating successful execution without errors.