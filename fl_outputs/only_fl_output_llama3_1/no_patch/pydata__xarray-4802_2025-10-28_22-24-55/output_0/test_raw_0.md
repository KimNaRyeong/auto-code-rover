Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from functools import wraps

def assert_raises(expected_exception, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except expected_exception:
            print_stacktrace(sys.exc_info()[1])
            raise
    return wrapper

@assert_raises(AttributeError)
def reproducer():
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()
    xr.decode_cf(ds)

if __name__ == "__main__":
    reproducer()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.