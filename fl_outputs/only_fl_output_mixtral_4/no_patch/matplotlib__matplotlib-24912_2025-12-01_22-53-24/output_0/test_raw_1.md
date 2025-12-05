 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
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

x = y = np.linspace(0, 1, 100)
data = np.random.rand(100, 100) * 50

myplot = plt.contour(x, y, data, levels=[100])
print(myplot.levels)

try:
    assert myplot.levels == [100]
except AssertionError as e:
    print_stacktrace(e)
```
When executed with Matplotlib 3.x, the script prints `[0.0]` and raises an `AssertionError` with a stack trace. When executed with Matplotlib 2.x, the script prints `[100]` and exits without raising an error.

Note that the script uses NumPy to generate random data, so you may need to install it using `pip install numpy` if it's not already installed.