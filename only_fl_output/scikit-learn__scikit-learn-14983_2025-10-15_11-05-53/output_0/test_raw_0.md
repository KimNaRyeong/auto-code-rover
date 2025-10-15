```python
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

def test_correct_repr():
    from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold

    expected_rkf = "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)"
    expected_rskf = "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)"

    rkf_repr = repr(RepeatedKFold())
    rskf_repr = repr(RepeatedStratifiedKFold())

    assert rkf_repr == expected_rkf, f"Incorrect __repr__ for RepeatedKFold: {rkf_repr}"
    assert rskf_repr == expected_rskf, f"Incorrect __repr__ for RepeatedStratifiedKFold: {rskf_repr}"

if __name__ == "__main__":
    try:
        test_correct_repr()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("No issue found.")
    exit(0)
```