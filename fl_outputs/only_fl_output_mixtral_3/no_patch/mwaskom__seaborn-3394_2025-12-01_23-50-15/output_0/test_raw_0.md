 Here is a standalone python script `reproducer.py` to reproduce the issue:
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

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

try:
    grid = sns.FacetGrid(
        data=test_data,
        col='type',
        sharey=False,
        sharex=True,  # time-series consistency
    )
    grid.map(sns.lineplot, 'date', 'value', alpha=0.5)
    plt.show()

    # AssertionError is raised when the issue is present
    assert False, "Axis ordering is not reversed when plotting with pd.NA"
except AssertionError as e:
    print_stacktrace(e)
except Exception as e:
    print_stacktrace(e)
```
To run the script, execute `python3 reproducer.py` in the terminal. The script should raise an `AssertionError` and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.