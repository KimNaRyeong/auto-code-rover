import time
import subprocess

def measure_import_time(module):
    command = f"python -c 'import {module}'"
    start_time = time.time()
    subprocess.run(command, shell=True)
    end_time = time.time()
    return end_time - start_time

xarray_import_time = measure_import_time('xarray')

print(f"xarray import time: {xarray_import_time:.2f}s")

if xarray_import_time > 1.0:
    try:
        assert False, "xarray import time is too high"
    except AssertionError as e:
        def print_stacktrace(e: Exception):
            import traceback
            import sys
            tb = traceback.extract_tb(e.__traceback__)
            print("Traceback (most recent call last):", file=sys.stderr)
            for frame in tb:
                line_number = frame.lineno
                code_context = frame.line.strip() if frame.line else "Unknown"
                print(f'  File "{frame.filename}"', file=sys.stderr)
                print(f"    {line_number}: {code_context}", file=sys.stderr)
            print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
        print_stacktrace(e)
        exit(1)

exit(0)
