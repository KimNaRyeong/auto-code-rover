Here is the reproducer script:

```python
import sympy.abc as abc
from reproducer import global_parameters

def main():
    with global_parameters.evaluate(False):
        x = abc.x + abc.x
        print(x)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script will raise an `AssertionError` if the issue is present, and it will print a stack trace of the issue. If the issue is fixed, it will simply exit with code 0.

Please note that you need to have the `reproducer.py` file in the root directory of your project for this script to work correctly.