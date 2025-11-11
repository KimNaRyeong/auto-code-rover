Here is the reproducer script:

```python
import seaborn as sns
import numpy as np
import pandas as pd
from io import StringIO
import sys
import traceback

def custom_min(x):
    return float(np.asarray(x).min())

tips = pd.read_csv(StringIO("day,tip\n0,5.45\n1,6.78\n2,7.23\n3,8.12\n4,9.34"))

try:
    sns.set()
    ax = sns.pointplot(x="day", y="tip", data=pd.DataFrame({'day': [0, 1, 2], 'tip': [5.45, 6.78, 7.23]}), estimator=custom_min)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Regression: pointplot and barplot raise when using a custom estimator")
```

This script should be executed by `python3 reproducer.py`.