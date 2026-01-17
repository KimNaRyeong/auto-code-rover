 Here is a standalone python script `reproducer.py` to reproduce the issue:
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
When executed with matplotlib version 3.6.1, this script should raise a `KeyError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 11, in <module>
    the_rc = plt.style.library["seaborn-colorblind"]
KeyError: 'seaborn-colorblind'
```
When executed with matplotlib version 3.4.3, this script should not raise any exceptions and should exit with code 0.