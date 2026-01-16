# reproducer.py
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

def main():
    # Simulating normal exception handling
    try:
        raise LookupError("A\nB\nC")
    except LookupError as e:
        normal_behavior = str(e)

    # Simulating pytest.raises behavior
    class DummyExceptionContext:
        def __init__(self, exc_type):
            self.exc_type = exc_type
            self.value = None

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_val, traceback):
            if exc_type == self.exc_type:
                self.value = exc_val
                return True # prevents the exception from propagating

    pytest_raises_behavior = ""
    with DummyExceptionContext(LookupError) as e:
        raise LookupError("A\nB\nC")
        pytest_raises_behavior = str(e.value)

    # The behavior should match the normal behavior
    assert pytest_raises_behavior == normal_behavior, "Mismatch in exception message representation"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1) from e
    else:
        print("Issue not detected. The behaviors match.")
        SystemExit(0)
