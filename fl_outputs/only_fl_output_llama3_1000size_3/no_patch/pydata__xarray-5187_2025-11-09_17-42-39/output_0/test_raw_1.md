Here is the reproducer script:

```python
import xarray as xr
import numpy as np
import dask.array as da
from functools import wraps

def raises_assertion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError:
            print_stacktrace(sys.exc_info()[1])
            raise
    return wrapper

@raises_assertion
def reproducer():
    data = np.random.rand(100)
    data[25] = np.nan
    da_data = xr.DataArray(data)

    # unchunked
    orig_value = da_data[25].values
    backfilled_value = da_data.bfill('dim_0')[25].values

    print(f'output : orig {orig_value}, backfill : {backfilled_value}')

    # small chunk
    da1 = da_data.chunk({'dim_0': 1})
    orig_value = da1[25].values
    backfilled_value = da1.bfill('dim_0')[25].values

    print(f'output chunks==1 : orig {orig_value}, backfill : {backfilled_value}')

    # medium chunk
    da1 = da_data.chunk({'dim_0': 10})
    orig_value = da1[25].values
    backfilled_value = da1.bfill('dim_0')[25].values

    print(f'output chunks==10 : orig {orig_value}, backfill : {backfilled_value}')

    assert backfilled_value == 0.024710724099643477, "Expected backfilled value to be 0.024710724099643477"

if __name__ == "__main__":
    reproducer()
```

This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue.