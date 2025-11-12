Here is the reproducer script:

```python
import numpy as np
from sklearn.impute import MissingIndicator
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    a = np.array([[c] for c in 'abcdea'], dtype=str)
    MissingIndicator().fit_transform(a)
    MissingIndicator(missing_values='a').fit_transform(a)
except Exception as e:
    print_stacktrace(e)
    raise
```

This script will reproduce the issue with non-numeric inputs when using `sklearn.impute.MissingIndicator`.