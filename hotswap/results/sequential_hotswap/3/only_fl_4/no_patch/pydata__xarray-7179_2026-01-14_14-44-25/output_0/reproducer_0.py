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

def main():
    start_time = time.time()
    import xarray
    end_time = time.time()
    import_duration = end_time - start_time
    print(f"xarray import time: {import_duration} seconds")

    # Change the threshold according to the issue description or your specific requirements
    threshold = 0.6  # Set a reasonable threshold for the import time

    try:
        assert import_duration < threshold, f"xarray import time exceeds {threshold} seconds"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
