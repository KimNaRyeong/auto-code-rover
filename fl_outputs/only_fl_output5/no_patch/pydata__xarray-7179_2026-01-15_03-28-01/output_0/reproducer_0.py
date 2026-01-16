import time
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def measure_import_time(module_name: str) -> float:
    start_time = time.time()
    __import__(module_name)
    end_time = time.time()
    return end_time - start_time

def test_import_time():
    xarray_import_time = measure_import_time("xarray")
    print(f"Xarray import time: {xarray_import_time:.3f} seconds")
    assert xarray_import_time < 1.0, "Xarray import time exceeds acceptable threshold."

if __name__ == "__main__":
    try:
        test_import_time()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not present. Xarray import time is within acceptable threshold.")
        sys.exit(0)
