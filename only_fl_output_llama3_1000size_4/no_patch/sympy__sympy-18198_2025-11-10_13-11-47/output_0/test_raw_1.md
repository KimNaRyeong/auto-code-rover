Here is the `reproducer.py` script:

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

def main():
    class GlobalParameters:
        def __init__(self):
            self._parameters = {'evaluate': [True], 'distribute': [True]}

        @property
        def evaluate(self):
            return self._parameters['evaluate'][0]

        @evaluate.setter
        def evaluate(self, value):
            self._parameters['evaluate'] = [value]

    global_parameters = GlobalParameters()

    with global_parameters.evaluate(False) as _:
        assert not global_parameters.evaluate, "Expected evaluate to be False"
    print_stacktrace(AssertionError)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            raise
    except Exception as e:
        print_stacktrace(e)
```

This script defines a `GlobalParameters` class that mimics the behavior described in the issue. It then uses this class to reproduce the issue and assert that `evaluate` is False, which should raise an `AssertionError`.