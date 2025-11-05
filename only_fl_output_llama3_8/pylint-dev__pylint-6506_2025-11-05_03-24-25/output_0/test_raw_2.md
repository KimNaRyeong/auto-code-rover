Here is the reproducer script:

```python
import sys
from pylint.lint import Run

def main():
    try:
        Run(['-Q', 'non_existent_file.py'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue should not be present")

if __name__ == "__main__":
    main()
```

This script runs `pylint` with the `-Q` option and a non-existent file. If the error occurs, it prints the stack trace and raises an `AssertionError`.