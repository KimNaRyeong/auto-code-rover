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

def test_issue():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.cm import get_cmap
    cmap = get_cmap('bwr_r')
    fig, ax = plt.subplots()
    x, y = np.mgrid[0:10:100j, 0:10:100j]
    v = np.abs(np.sin(x) * np.cos(y))
    c = (cmap(v[:-1, :-1]) * 255).astype(np.int64)
    try:
        ax.pcolorfast(x, y, c)
        # Expected to raise ValueError: RGBA values should be within 0-1 range
        print("Error: Expected exception not raised")
        exit(1)
    except ValueError as e:
        assert "RGBA values should be within 0-1 range" in str(e), "Unexpected error message"
        # If the issue is fixed, this point should not be reached; exit with code 0
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    test_issue()
```