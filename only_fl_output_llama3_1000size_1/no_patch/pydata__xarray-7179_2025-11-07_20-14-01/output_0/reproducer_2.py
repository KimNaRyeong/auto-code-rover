import time
from functools import wraps

def measure_import_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Importing xarray took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@measure_import_time
def reproduce_issue():
    import time
    time.sleep(1.5)  # Simulate the long import time
    raise AssertionError("Expected import time to be shorter")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
