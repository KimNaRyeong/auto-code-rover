Here is the reproducer script:

```python
import time
import xarray as xr
from functools import wraps

def measure_import_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Importing xarray took {end - start:.2f} seconds")
        if end - start > 1.5:
            raise AssertionError("Importing xarray takes too long")
    return wrapper

@measure_import_time
def main():
    import xarray

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script defines a decorator `measure_import_time` that measures the time it takes to execute the decorated function. The `main` function is then decorated with this decorator and imports xarray. If the import time exceeds 1.5 seconds, an AssertionError is raised, which will be caught by the main block of code and print the stack trace using the provided function.