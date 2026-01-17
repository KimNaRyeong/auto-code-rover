# reproducer.py
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

def test_pipeline_sample_weight_issue():
    try:
        from sklearn.pipeline import make_pipeline
        from sklearn.linear_model import LogisticRegression
        clf = make_pipeline(LogisticRegression())
        # This call should not cause an issue if the error message has been appropriately updated.
        clf.fit([[0], [0]], [0, 1], sample_weight=[1, 1])
    except ValueError as e:
        # Check if the error message is the old, unclear one.
        if 'not enough values to unpack' in str(e):
            print_stacktrace(e)
            raise AssertionError(
                "The issue is present: Error message does not describe the correct format for passing sample_weight to a step in a Pipeline.")
        else:
            # Consider any other ValueError as unrelated to the specific issue we're looking for.
            print("An error occurred, but it's not related to the specific issue in question.")
            sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred.")
    else:
        print("The issue seems to have been fixed - no error when passing sample_weight directly.")
        sys.exit(0)

if __name__ == "__main__":
    test_pipeline_sample_weight_issue()
