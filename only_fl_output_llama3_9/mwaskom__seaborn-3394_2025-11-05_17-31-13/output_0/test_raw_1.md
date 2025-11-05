Here is the reproducer script:

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import sys
import traceback

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

def reproduce_issue():
    try:
        mock_data = pd.DataFrame({
            'date': ['0', '1', '2', '3'],
            'value': [1, 2, np.nan, 1.5]
        })

        test_data = pd.concat([mock_data, mock_data.copy(), mock_data.copy()])

        grid = sns.FacetGrid(
            data=test_data,
            col='date',
            sharey=False,
            sharex=True
        )
        grid.map(sns.lineplot, 'value', alpha=0.5)
        plt.show()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

reproduce_issue()
```

This script will reproduce the issue and print a stack trace if it fails to produce the expected result.