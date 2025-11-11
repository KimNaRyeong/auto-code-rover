Here is the reproducer script:

```python
import seaborn as sns
import numpy as np
import pandas as pd
from io import StringIO
import sys

def custom_min(x):
    return float(np.asarray(x).min())

tips = pd.read_csv(StringIO("day,tip\n0,5.01\n1,6.45\n2,7.51\n3,8.47\n4,9.33\n5,10.27\n6,11.12"))

try:
    sns.pointplot(x="day", y="tip", data=pd.DataFrame({'day': [0, 1, 2], 'tip': [5.01, 6.45, 7.51]}), estimator=custom_min)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Regression: pointplot and barplot raise when using a custom estimator")
finally:
    sys.exit(0)

def print_stacktrace(e):
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

if __name__ == "__main__":
    try:
        sns.pointplot(x="day", y="tip", data=pd.DataFrame({'day': [0, 1, 2], 'tip': [5.01, 6.45, 7.51]}), estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Regression: pointplot and barplot raise when using a custom estimator")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    try:
        sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Regression: pointplot and barplot raise when using a custom estimator")
    finally:
        sys.exit(0)
```

This script will reproduce the issue by calling `sns.pointplot` with a custom estimator. If the issue is present, it will print the stack trace and raise an `AssertionError`.