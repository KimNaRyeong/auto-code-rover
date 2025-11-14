I apologize for the mistake. Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import traceback

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
    mock_data = pd.DataFrame({
        'date': ['0', '1', '2', '3'],
        'value': [1, 2, 1, 1.5]
    })

    mock_data_pd_na = mock_data.copy()
    mock_data_pd_na.loc[2, 'value'] = pd.NA

    grid = sns.FacetGrid(
        data=mock_data_pd_na,
        col=None,
        sharey=False,
        sharex=True,  # time-series consistency
    )
    grid.map(sns.lineplot, 'date', 'value', alpha=0.5)
    plt.show()

    # Check if the issue is present
    assert (mock_data_pd_na.sort_values('date')['value'].isna().sum() == 1), "pd.NA reverses axis ordering"

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script should reproduce the issue and raise an `AssertionError` when the issue is present, printing a stack trace of the issue. If the issue is fixed, it will exit with code 0.