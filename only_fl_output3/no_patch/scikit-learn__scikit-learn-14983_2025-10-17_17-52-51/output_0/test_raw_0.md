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

def check_repr_correctness():
    from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold

    expected_rkf_repr = "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)"
    actual_rkf_repr = repr(RepeatedKFold())
    assert actual_rkf_repr == expected_rkf_repr, f"RepeatedKFold __repr__ incorrect. Expected: {expected_rkf_repr}, Got: {actual_rkf_repr}"

    expected_rskf_repr = "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)"
    actual_rskf_repr = repr(RepeatedStratifiedKFold())
    assert actual_rskf_repr == expected_rskf_repr, f"RepeatedStratifiedKFold __repr__ incorrect. Expected: {expected_rskf_repr}, Got: {actual_rskf_repr}"

if __name__ == "__main__":
    try:
        check_repr_correctness()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error if the assertion fails
    print("No issues detected.")
    exit(0)  # Exit successfully if the issue is not present
```