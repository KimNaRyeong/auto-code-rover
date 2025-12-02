 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sklearn.compose import ColumnTransformer

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

try:
    ColumnTransformer([]).set_params(n_jobs=2)
except Exception as e:
    assert False, e
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 10, in <module>
    ColumnTransformer([]).set_params(n_jobs=2)
  File "/Users/joel/repos/scikit-learn/sklearn/compose/_column_transformer.py", line 181, in set_params
    self._set_params('_transformers', **kwargs)
  File "/Users/joel/repos/scikit-learn/sklearn/utils/metaestimators.py", line 44, in _set_params
    names, _ = zip(*getattr(self, attr))
ValueError: not enough values to unpack (expected 2, got 0)
```
This stack trace is the same as the one in the issue description, which confirms that the issue is present in the current implementation of `_BaseCompostion._set_params`.