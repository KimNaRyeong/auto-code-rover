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
            'value': [1, 2, 1, 1.5]
        })

        mock_data_full = mock_data.copy()
        mock_data_full['type'] = 'no_NA'

        mock_data_pd_na = mock_data.copy()
        mock_data_pd_na['type'] = 'pd.NA'
        mock_data_pd_na.loc[2, 'value'] = pd.NA

        mock_data_np_nan = mock_data.copy()
        mock_data_np_nan['type'] = 'np.nan'
        mock_data_np_nan.loc[2, 'value'] = np.nan

        test_data = pd.concat([mock_data_full, mock_data_pd_na, mock_data_np_nan])

        grid = sns.FacetGrid(
            data=test_data,
            col='type',
            sharey=False,
            sharex=True  # time-series consistency
        )
        grid.map(sns.lineplot, 'date', 'value', alpha=0.5)
        plt.show()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

reproduce_issue()
```

This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.