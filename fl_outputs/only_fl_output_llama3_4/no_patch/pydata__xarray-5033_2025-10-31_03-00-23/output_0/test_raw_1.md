It seems that the issue is not related to adding custom backends in xarray, but rather it's an issue with numpy. The error message suggests that `np.unicode_` was removed in the NumPy 2.0 release and you should use `np.str_` instead.

Here is a reproducer script for this issue:

```python
import numpy as np

def main():
    try:
        print(np.unicode_)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected AttributeError"

if __name__ == "__main__":
    main()
```

This script attempts to access `np.unicode_`, which should raise an `AttributeError` because it was removed in the NumPy 2.0 release.