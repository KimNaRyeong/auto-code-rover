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

def test_reproducer():
    try:
        from sklearn.ensemble import RandomForestClassifier
        est = RandomForestClassifier(n_estimators=100, random_state=42, bootstrap=False, n_jobs=-1)
        est.fit([[0, 0], [0, 1]], [["red", "blue"], ["green", "green"]])
        est.predict([[1, 1]])
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected ValueError"

if __name__ == "__main__":
    test_reproducer()
