Here is the reproducer script:

```python
import time
import xarray as xr
import pandas as pd
import scipy
import numpy
import datetime
from functools import wraps

def timed_import(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f}s")
        return result
    return wrapper

@timed_import
def import_xarray():
    import xarray

@timed_import
def import_pandas():
    import pandas

@timed_import
def import_scipy():
    import scipy

@timed_import
def import_numpy():
    import numpy

@timed_import
def import_datetime():
    import datetime

try:
    import_xarray()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("xarray imported successfully")
```

This script defines a decorator `timed_import` that measures the time it takes to execute an imported function. It then uses this decorator to measure the time taken by importing xarray, pandas, scipy, numpy and datetime.

If the import of xarray takes more than 1 second, the script will raise an AssertionError and print the stack trace using the provided `print_stacktrace` function.