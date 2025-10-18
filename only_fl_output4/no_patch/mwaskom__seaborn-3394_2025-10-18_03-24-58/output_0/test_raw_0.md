```python
# reproducer.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def print_stacktrace(e: Exception):
    import traceback
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
    grid.map(sns.lineplot, 'date', 'value', alpha=0.5)
    try:
        # Extract axis limits to assert if the ordering gets reversed
        axes = grid.axes.flatten()
        y_limits_no_na = axes[0].get_ylim()
        y_limits_pd_na = axes[1].get_ylim()
        y_limits_np_nan = axes[2].get_ylim()
        
        # Assert ascending order for y-axis limits, since seaborn should handle NAs uniformly without reversing axis
        assert y_limits_no_na == y_limits_pd_na == y_limits_np_nan, "Axis ordering gets reversed with pd.NA"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not present, axis order is as expected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```