# reproducer.py

def main():
    try:
        from sklearn.compose import ColumnTransformer
        # Attempt to set_params on a ColumnTransformer with no estimators
        ColumnTransformer([]).set_params(n_jobs=2)
        # If the ValueError is not raised, it means the issue has been fixed
        print("Issue fixed.")
        exit(0)
    except Exception as e:
        # Catch any exception that is not a ValueError indicating the specific issue
        if isinstance(e, ValueError) and "not enough values to unpack" in str(e):
            pass  # This is the expected error for the issue, so don't assert here.
        else:
            # If any other error or if the error message doesn't match, then it's unexpected.
            print_stacktrace(e)
            assert False, "An unexpected exception occurred."

        # Correctly caught the expected ValueError for the issue
        print_stacktrace(e)
        assert "not enough values to unpack" in str(e), "The issue is present."

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

if __name__ == "__main__":
    main()
