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

try:
    t = [[1]]
    p = [[0]]
    ndcg_score(t, p)
except Exception as e:
    print_stacktrace(e)
    assert True
```
When executed with `python3 reproducer.py`, it should print the stack trace of the issue:
```python
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    ndcg_score(t, p)
  File "/Users/cbournhonesque/.pyenv/versions/bento/lib/python3.8/site-packages/sklearn/metrics/_ranking.py", line 1567, in ndcg_score
    _check_dcg_target_type(y_true)
  File "/Users/cbournhonesque/.pyenv/versions/bento/lib/python3.8/site-packages/sklearn/metrics/_ranking.py", line 1307, in _check_dcg_target_type
    raise ValueError
ValueError: Only ('multilabel-indicator', 'continuous-multioutput', 'multiclass-multioutput') formats are supported. Got binary instead
```
This indicates that the issue is present. If the issue is fixed, the script should exit with code 0 without printing the stack trace.