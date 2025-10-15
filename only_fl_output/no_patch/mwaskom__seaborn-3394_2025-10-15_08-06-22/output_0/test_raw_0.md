```python
# reproducer.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

def main():
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
        sharex=True,  # time-series consistency
    )
    plot = grid.map(sns.lineplot, 'date', 'value', alpha=0.5)

    # Check if the axis are ordered as expected
    # This part assumes that y-axis limits are available and compares them
    limits_no_NA = grid.facet_axis(0, 0).get_ylim()
    limits_pd_NA = grid.facet_axis(0, 1).get_ylim()
    limits_np_nan = grid.facet_axis(0, 2).get_ylim()

    try:
        # If the issue is present, the y-axis limits for pd.NA should be reversed compared to others
        assert limits_no_NA == limits_pd_NA == limits_np_nan, "Y-axis limits are not consistent across plots."
    except AssertionError as e:
        print_stacktrace(e)
        raise

try:
    main()
except AssertionError:
    plt.show()  # Show the plot for visual inspection, if needed
    exit(1)
else:
    print("Issue not reproduced. The plot y-axis ordering is consistent as expected.")
    exit(0)
```