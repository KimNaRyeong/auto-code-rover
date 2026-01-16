```python
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
    from sklearn.pipeline import make_pipeline
    from sklearn.linear_model import LogisticRegression

    try:
        clf = make_pipeline(LogisticRegression())
        # Attempt passing sample_weight directly, which is expected to raise an error.
        clf.fit([[0], [0]], [0, 1], sample_weight=[1, 1])
    except ValueError as err:
        if "not enough values to unpack" in str(err):
            # Expected error message, but it's not user-friendly.
            # This error is part of the issue we're trying to reproduce.
            print_stacktrace(err)
            raise AssertionError("Unfriendly error message as described in the issue reproduced successfully.")
    
    # If the code reaches this point without an error, the issue is not present, 
    # which means it might have been fixed or the behavior changed.
    print("The issue does not reproduce. Exiting normally.")
    exit(0)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(e)
        exit(1)
```

In this script, `main()` function tries to reproduce the issue described by attempting to fit a `LogisticRegression` model inside a `Pipeline` with an incorrect usage of `sample_weight`. The expectation is that a `ValueError` will be raised because `sample_weight` is not prefixed with the step name, which is the correct usage. The script checks for the presence of a specific substring in the error message to confirm if the thrown error matches the expected non-friendly error message. If this specific error is caught, it prints a detailed stack trace using `print_stacktrace` and raises an `AssertionError` to indicate the issue has been reproduced. If the script runs without encountering this error, it might mean the issue has been resolved, and it exits normally.