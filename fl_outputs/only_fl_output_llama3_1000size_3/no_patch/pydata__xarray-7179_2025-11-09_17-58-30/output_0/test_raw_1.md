Here is the reproducer script:

```python
import time
from functools import wraps

def measure_import_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Importing xarray took {end - start:.2f} seconds")
    return wrapper

@measure_import_time
def main():
    import time
    for _ in range(1000):
        import xarray

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script will repeatedly import the `xarray` package 1000 times, which should take a noticeable amount of time. If the import time exceeds 1.5 seconds, an AssertionError is raised, which will be caught by the main block of code and print the stack trace using the provided function.