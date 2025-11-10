Here is the reproducer script:

```python
import os
import sys
from pylint_quotes.checker import Checker  # noqa: F401

def main():
    try:
        os.system('python -m venv venv && . venv/bin/activate && pip install -r requirements.txt')
        os.system('pylint --rcfile pylintrc demo.py')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError('Issue not fixed')

if __name__ == '__main__':
    main()
```

This script creates a virtual environment, installs the required packages, and then runs `pylint` with the given configuration. If an exception is raised during this process, it prints the stack trace using the provided function and raises an `AssertionError`.