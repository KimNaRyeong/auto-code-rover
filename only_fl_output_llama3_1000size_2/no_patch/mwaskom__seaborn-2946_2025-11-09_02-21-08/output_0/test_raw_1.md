Here is the reproducer script:

```python
import seaborn as sns
import numpy as np
import pandas as pd
from io import StringIO
from functools import wraps

def custom_min(x):
    return float(np.asarray(x).min())

tips = pd.read_csv(StringIO("day,tip\n0,5.0\n1,6.0\n2,7.0\n3,8.0\n4,9.0"))

try:
    sns.pointplot(x="day", y="tip", data=tips.groupby("day")["tip"].apply(custom_min))
except Exception as e:
    print_stacktrace(e)
    assert False, "Regression: pointplot and barplot raise when using a custom estimator"
```

This script will reproduce the issue by creating a pandas DataFrame from a string, then attempting to create a point plot with the `pointplot` function. If the error occurs, it will print the stack trace and fail the assertion, indicating that the regression is present.

Please note that this reproducer requires matplotlib installed in your environment.