Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import xarray as xr

def reproduce_issue():
    ds = xr.tutorial.open_dataset("air_temperature")
    try:
        ds.weighted(xr.ones_like(ds["air"])).mean("dummy")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

To run the reproducer, execute `python3 reproducer.py` in your terminal. If the issue is present, it should print a stack trace and exit with code 1.