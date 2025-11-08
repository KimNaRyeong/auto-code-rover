Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import numpy as np
from astropy import units as u

def main():
    try:
        array_equal = np.array_equal([1, 2, 3] * u.mm, [1, 2, 3] * u.s)
        assert not array_equal, "Issue should return False"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue should not be raised")

if __name__ == "__main__":
    main()
```

This script attempts to call `np.array_equal()` on two arrays of different units (`u.mm` and `u.s`). If the function returns `True`, it raises an `AssertionError`.