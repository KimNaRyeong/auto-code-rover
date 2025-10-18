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

def test_range_slider_init_value():
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.widgets import RangeSlider

        # generate a fake image
        np.random.seed(19680801)
        N = 128
        img = np.random.randn(N, N)

        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        fig.subplots_adjust(bottom=0.25)

        slider_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
        slider = RangeSlider(slider_ax, "Threshold", img.min(), img.max(), valinit=[0.0, 0.0])

        assert slider.val == (0.0, 0.0), "RangeSlider did not initialize with given values."
        
        print("Test passed: RangeSlider initialized with given values.")

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("RangeSlider initialization with given values failed.") from e

if __name__ == "__main__":
    test_range_slider_init_value()
```

This `reproducer.py` script attempts to create a `RangeSlider` with an initial value and checks if it was successfully set to the specified value. It outputs an assertion error and a stack trace if the script encounters the reported issue, specifically an `IndexError` due to an index out of bounds when running with a Matplotlib version where the bug is present. When the issue is fixed (e.g., after commenting the problematic line as suggested or by using a version of Matplotlib where this has been corrected), the assert statement should pass, and the script will confirm that the "Test passed" indicating the issue has been resolved.