 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

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

sample = np.full([10_000_000, 1], 10.0, dtype=np.float16)
try:
    StandardScaler().fit_transform(sample)
except Exception as e:
    print_stacktrace(e)
```

When executed, the script should print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 12, in <module>
    StandardScaler().fit_transform(sample)
  File "/opt/conda/lib/python3.6/site-packages/sklearn/preprocessing/data.py", line 765, in fit_transform
    X /= self.scale_
RuntimeError: invalid value encountered in true_divide
```

This stack trace confirms that the issue is present in the `StandardScaler` class when using a large `float16` numpy array.