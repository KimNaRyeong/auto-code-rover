Here is the reproducer script:

```python
import sympy
from sympy.ntheory.digits import digits

def test_digits():
    result = digits(-1, 2, bits=3)
    assert len(result) == 3 and result[0] == -2, "Expected [-2, 0, 1], got {}".format(result)

try:
    test_digits()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    exit(0)
```

This script will run the `test_digits` function and check if the result is correct. If not, it will raise an `AssertionError`, which will be caught by the script and printed with a stack trace.