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

def reproduce_issue():
    try:
        from sklearn.pipeline import make_pipeline
        from sklearn.linear_model import LogisticRegression

        clf = make_pipeline(LogisticRegression())
        clf.fit([[0], [0]], [0, 1], logisticregression__sample_weight=[1, 1])
        clf.fit([[0], [0]], [0, 1], sample_weight=[1, 1])
        
        # If no exception is raised, then we assert False to indicate the test should fail.
        assert False, "Expected a ValueError regarding incorrect parameter format, but none was raised."
    except Exception as e:
        try:
            # Expected exception assertion
            assert "ValueError: not enough values to unpack (expected 2, got 1)" in str(e), "Unexpected error message"
        except AssertionError as ae:
            # If the assertion about the exception message fails, print stack trace of the AssertionError
            print_stacktrace(ae)
            exit(1)
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
