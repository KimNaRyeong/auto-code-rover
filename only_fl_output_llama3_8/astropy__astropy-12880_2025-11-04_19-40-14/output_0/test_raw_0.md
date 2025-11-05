Here is the reproducer script:

```python
import os
import astropy.timeseries as ats
from astropy.io import ascii

def main():
    # Create a BinnedTimeSeries object with datetime column
    time_bin_start = [datetime64('2022-01-01 00:00:00'), datetime64('2022-01-02 00:00:00')]
    my_binned_time_series = ats.BinnedTimeSeries(time_bin_start, ...)

    # Write the BinnedTimeSeries object to an ECSV file
    my_binned_time_series.write('test.ecsv', format='ascii.ecsv')

    # Try to read the ECSV file back into a BinnedTimeSeries object
    try:
        tsrbin = ats.BinnedTimeSeries.read('test.ecsv', format='ascii.ecsv')
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Failed to read ECSV file")

if __name__ == "__main__":
    main()
```

This script creates a `BinnedTimeSeries` object with a datetime column, writes it to an ECSV file, and then tries to read the file back into another `BinnedTimeSeries` object. If the reading fails due to the strict type checking in ECSV, the script prints the stack trace and raises an `AssertionError`.