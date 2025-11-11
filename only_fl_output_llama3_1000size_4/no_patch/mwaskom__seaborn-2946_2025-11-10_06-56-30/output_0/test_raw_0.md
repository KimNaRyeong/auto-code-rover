Here is the reproducer script:

```python
import seaborn as sns
import numpy as np
import pandas as pd
from io import StringIO

def custom_min(x):
    return float(np.asarray(x).min())

tips = pd.read_csv(StringIO("day,tip\n0,5.0\n1,6.0\n2,7.0\n3,8.0\n4,9.0"))

try:
    ax = sns.pointplot(x="day", y="tip", data=tips, estimator=custom_min)
except Exception as e:
    print_stacktrace(e)
    assert False, "Regression: pointplot and barplot raise when using a custom estimator"
```

This script will reproduce the issue by calling `pointplot` with the custom `min` function. The `print_stacktrace` function is used to print the stack trace of the exception. If the issue is present, the script will raise an `AssertionError`.