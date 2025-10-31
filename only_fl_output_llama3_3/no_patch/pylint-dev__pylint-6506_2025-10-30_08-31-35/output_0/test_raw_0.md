Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sys
from pylint.lint import Run

def main():
    try:
        Run(['-Q'])  # This should raise an UnrecognizedOptionError
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected UnrecognizedOptionError"

if __name__ == "__main__":
    main()
```

This script uses the `Run` class from pylint to run a lint command with the `-Q` option. This should raise an `UnrecognizedOptionError`, which is then caught and printed using the provided `print_stacktrace` function. The script also asserts that the error was raised, indicating that the issue is present.

To reproduce the issue, simply execute this script: `python3 reproducer.py`. If the issue is fixed, the script will exit with code 0; otherwise, it will raise an `AssertionError` and print a stack trace.