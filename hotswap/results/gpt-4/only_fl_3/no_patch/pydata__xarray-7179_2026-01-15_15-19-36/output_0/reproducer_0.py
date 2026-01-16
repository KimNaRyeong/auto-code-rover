import time
import subprocess
import sys

def measure_import_time(module_name: str) -> float:
    start_time = time.time()
    subprocess.run([sys.executable, "-c", f"import {module_name}"], capture_output=True)
    end_time = time.time()
    return end_time - start_time

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

def test_import_time():
    module_name = "xarray"
    threshold = 1.0  # seconds, adjust this threshold based on acceptable performance criteria
    import_time = measure_import_time(module_name)

    try:
        assert import_time < threshold, f"Importing {module_name} took too long: {import_time:.3f} seconds"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status if the import time exceeds the threshold
    else:
        print(f"Importing {module_name} is within acceptable threshold: {import_time:.3f} seconds")
        sys.exit(0)  # Success

if __name__ == "__main__":
    test_import_time()
