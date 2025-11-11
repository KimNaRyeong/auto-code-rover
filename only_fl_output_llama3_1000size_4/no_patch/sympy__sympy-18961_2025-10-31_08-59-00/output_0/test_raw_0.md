Here is the reproducer script:

```python
import sympy
from sympy.ntheory.digits import digits

def main():
    try:
        result = digits(-1, 2, bits=3)
        assert len(result) == 3, "Expected length of {} but got {}".format(3, len(result))
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` if the issue is present. The stack trace will be printed and the script will exit with code 0 when the issue is fixed.