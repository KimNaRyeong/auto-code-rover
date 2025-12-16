 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.pyplot as plt

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
    the_rc = plt.style.library["seaborn-colorblind"]
except Exception as e:
    print_stacktrace(e)
    assert False
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 10, in <module>
    the_rc = plt.style.library["seaborn-colorblind"]
KeyError: 'seaborn-colorblind'
```
This reproduces the issue where setting `matplotlib.pyplot.style.library['seaborn-colorblind']` results in a `KeyError` on `matplotlib` version 3.6.1. The expected outcome is that `seaborn-colorblind` should be set as the `matplotlib` library style and the script should continue plotting with that style.