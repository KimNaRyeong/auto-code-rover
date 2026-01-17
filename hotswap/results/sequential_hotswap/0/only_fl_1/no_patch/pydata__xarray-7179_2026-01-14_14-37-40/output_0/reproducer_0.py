import time
import subprocess
import sys

def measure_import_time(module_name: str) -> float:
    start_time = time.time()
    subprocess.run([sys.executable, "-c", f"import {module_name}"], check=True)
    return time.time() - start_time

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

def check_import_time(module_name: str, max_allowed_time: float):
    try:
        import_time = measure_import_time(module_name)
        assert import_time < max_allowed_time, f"Importing {module_name} took too long ({import_time} seconds), which exceeds the allowed time of {max_allowed_time} seconds."
        print(f"Import time for {module_name} is within the acceptable range ({import_time} seconds).")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    MODULE_NAME = "xarray"
    MAX_ALLOWED_TIME = 1.0  # seconds; you might adjust this threshold as per your requirements
    
    check_import_time(MODULE_NAME, MAX_ALLOWED_TIME)
