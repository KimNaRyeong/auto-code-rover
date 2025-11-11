Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
import sys
from pylint.lint import Run

def main():
    try:
        # Set up the environment
        venv_path = 'venv'
        if not os.path.exists(venv_path):
            raise AssertionError(f"Virtual environment does not exist at {venv_path}")

        # Install the requirements
        if not os.path.exists('requirements.txt'):
            raise AssertionError("Requirements file does not exist")

        try:
            os.system(f'python -m venv {venv_path}')
            os.system(f'{os.path.join(venv_path, "bin", "activate")}; pip install -r requirements.txt')
        except Exception as e:
            print_stacktrace(e)
            sys.exit(1)

        # Run pylint with the given configuration
        try:
            os.system('pylint --rcfile pylintrc demo.py')
        except Exception as e:
            print_stacktrace(e)
            sys.exit(1)

    except AssertionError as e:
        raise AssertionError(str(e))

if __name__ == '__main__':
    main()
```

This script sets up a virtual environment, installs the required packages, and then runs pylint with the given configuration. If any of these steps fail, it prints the stack trace and exits with code 1.

To reproduce the issue, simply run this script using Python: `python3 reproducer.py`.