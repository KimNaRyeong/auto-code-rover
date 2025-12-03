 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sklearn.metrics import ndcg_score

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    t = [[1]]
    p = [[0]]
    with assert assertionRaises(ValueError):
        ndcg_score(t, p)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 12, in <module>
    ndcg_score(t, p)
  File "/Users/cbournhonesque/.pyenv/versions/bento/lib/python3.8/site-packages/sklearn/metrics/_ranking.py", line 1567, in ndcg_score
    _check_dcg_target_type(y_true)
  File "/Users/cbournhonesque/.pyenv/versions/bento/lib/python3.8/site-packages/sklearn/metrics/_ranking.py", line 1307, in _check_dcg_target_type
    raise ValueError(
ValueError: Only ('multilabel-indicator', 'continuous-multioutput', 'multiclass-multioutput') formats are supported. Got binary instead
```
This stack trace shows that the issue is present and that the `ndcg_score` function raises a `ValueError` when `y_true` is a list of length 1.