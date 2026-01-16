```python
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

def test_scatter_3d_nan_handling():
    import numpy as np
    from matplotlib import pylab as plt
    try:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        # This line should not raise a ValueError
        ax.scatter([1,np.nan,3], [2,np.nan,4], [3, np.nan,5], color=[[.5,.5,.5,.5]]*3, s=11.5)
        plt.close(fig)  # Close the plot to prevent it from showing during tests
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present") from e

if __name__ == "__main__":
    test_scatter_3d_nan_handling()
```