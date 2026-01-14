# reproducer.py
def main():
    try:
        from sklearn.ensemble import AdaBoostClassifier
        clf = AdaBoostClassifier(base_estimator=None)
        clf.fit([[1]], [0])
        print("Issue not present, AdaBoostClassifier accepted base_estimator=None without errors.")
    except Exception as e:
        assert "InvalidParameterError" in str(e), "Unexpected error."
        print_stacktrace(e)
        print("AssertionError: Issue with 'base_estimator=None' setting is present.")


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
