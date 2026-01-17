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
    from sklearn.compose import ColumnTransformer

    try:
        # Attempt to reproduce the reported issue
        ct = ColumnTransformer([]).set_params(n_jobs=2)
    except ValueError as e:
        # When the error occurs, print the stack trace
        print_stacktrace(e)
        # An AssertionError is raised to indicate the presence of the issue
        raise AssertionError("The issue is present.")

    # If the ColumnTransformer initiation and parameter setting succeeds,
    # it means the issue has been resolved.
    print("The issue has been fixed.")

if __name__ == "__main__":
    main()
