Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import astropy
from astropy.timeseries import BinnedTimeSeries

def main():
    try:
        bts = BinnedTimeSeries.read('test.ecsv', format='ascii.ecsv')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to read ECSV file")

if __name__ == "__main__":
    main()
```

This script attempts to read an ECSV file using the `BinnedTimeSeries` class from Astropy. If the reading fails due to the strict type checking issue, it prints a stack trace and raises an `AssertionError`.