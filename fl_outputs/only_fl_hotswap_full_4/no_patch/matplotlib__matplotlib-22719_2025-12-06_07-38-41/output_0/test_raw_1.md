 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
import matplotlib as mpl

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

mpl.rcParams['axes.units'] = ['a', 'b']
f, ax = plt.subplots()
try:
    ax.plot([], [])
except Exception as e:
    print_stacktrace(e)
    assert False
```
The output of running `python3 reproducer.py` is:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 12
    ax.plot([], [])
  File "/Users/user/miniconda3/envs/seaborn-py3