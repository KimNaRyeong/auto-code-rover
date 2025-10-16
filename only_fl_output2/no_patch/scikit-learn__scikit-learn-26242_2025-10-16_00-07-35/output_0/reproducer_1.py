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
    try:
        from sklearn.ensemble import AdaBoostClassifier
        # Attempt to initialize AdaBoostClassifier with base_estimator set to None
        clf = AdaBoostClassifier(base_estimator=None)
        clf.fit([[1]], [0])  # Trigger the fitting process with minimal example data
        print("No exception raised. Issue appears to be fixed.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "The AdaBoostClassifier 'base_estimator=None' issue is present."

if __name__ == "__main__":
    main()
