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
    from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold
    try:
        assert repr(RepeatedKFold()) == "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)", "RepeatedKFold __repr__ incorrect"
        assert repr(RepeatedStratifiedKFold()) == "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)", "RepeatedStratifiedKFold __repr__ incorrect"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exits with a non-zero code if there is an assertion error
    print("No issues detected.")
    exit(0)

if __name__ == "__main__":
    main()
```