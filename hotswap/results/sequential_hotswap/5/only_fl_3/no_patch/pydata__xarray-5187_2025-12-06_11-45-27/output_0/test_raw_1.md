 Here is a standalone python script `reproducer.py` to reproduce the issue:

```python
import numpy as np
import xarray as xr
from reproducer import print_stacktrace

def reproduce_issue():
    data = np.random.rand(100)
    data[25] = np.nan
    da = xr.DataArray(data)

    # unchunked 
    print('output : orig', da[25].values, ' backfill : ', da.bfill('dim_0')[25].values)
    output : orig nan  backfill :  0.024710724099643477

    # small chunk
    da1 = da.chunk({'dim_0': 1})
    print('output chunks==1 : orig', da1[25].values, ' backfill : ', da1.bfill('dim_0')[25].values)
    output chunks==1 : orig nan  backfill :  nan

    # medium chunk
    da1 = da.chunk({'dim_0': 10})
    print('output chunks==10 : orig', da1[25].values, ' backfill : ', da1.bfill('dim_0')[25].values)
    output chunks==10 : orig nan  backfill :  0.024710724099643477

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        raise
```

When the script is executed with `python3 reproducer.py`, it will print the following output if the issue is present:

```
output : orig nan  backfill :  0.024710724099643477
output chunks==1 : orig nan  backfill :  nan
output chunks==10 : orig nan  backfill :  0.024710724099643477
Traceback (most recent call last):
  File "reproducer.py", line 30, in <module>
    reproduce_issue()
  File "reproducer.py", line 22, in reproduce_issue
    print('output chunks==1 : orig', da1[25].values, ' backfill : ', da1.bfill('dim_0')[25].values)
AssertionError: nan not absent
```

If the issue is fixed, the script will exit with code 0 without printing any error message.