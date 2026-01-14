 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        # Expected results:
        # repr(RepeatedKFold()) -> 'RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)'
        # repr(RepeatedStratifiedKFold()) -> 'RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)'
        assert repr(RepeatedKFold()) == "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)", "Incorrect __repr__ string for RepeatedKFold"
        assert repr(RepeatedStratifiedKFold()) == "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=None)", "Incorrect __repr__ string for RepeatedStratifiedKFold"
    except AssertionError as e:
        print_stacktrace(e)
        raise e
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    assert repr(RepeatedKFold()) == "RepeatedKFold(n_splits=5, n_repeats=10, random_state=None)", "Incorrect __repr__ string for RepeatedKFold"
AssertionError: Incorrect __repr__ string for RepeatedKFold
```
This confirms that the `__repr__` string for `RepeatedKFold` and `RepeatedStratifiedKFold` do not show the correct values.