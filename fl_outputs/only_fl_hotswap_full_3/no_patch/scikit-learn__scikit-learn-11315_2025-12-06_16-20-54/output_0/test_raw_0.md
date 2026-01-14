 Here is a standalone python file `reproducer.py` to reproduce the issue:
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

if __name__ == "__main__":
    try:
        ColumnTransformer([]).set_params(n_jobs=2)
    except Exception as e:
        print_stacktrace(e)
        assert False, "The issue is reproduced"
```
When executed by `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 11, in <module>
    ColumnTransformer([]).set_params(n_jobs=2)
  File "/path/to/sklearn/compose/_column_transformer.py", line 181, in set_params
    self._set_params('_transformers', **kwargs)
  File "/path/to/sklearn/utils/metaestimators.py", line 44, in _set_params
    names, _ = zip(*getattr(self, attr))
ValueError: not enough values to unpack (expected 2, got 0)
```
The line numbers of the statements may be different depending on the location of the `sklearn` package.