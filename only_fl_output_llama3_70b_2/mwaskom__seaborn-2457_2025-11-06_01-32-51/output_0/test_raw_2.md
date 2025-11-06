Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

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

try:
    sns.set()
    fig, ax = plt.subplots()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sns.lineplot(x=[1, 1, 2, 2], y=[1, 2, 3, 4], ci=None)
        if not any("ci must be a positive scalar or None" in str(ww.message) for ww in w):
            raise AssertionError("Issue is present")
except Exception as e:
    print_stacktrace(e)
    raise
else:
    print("Issue is fixed")
```
<|start_header_id|>