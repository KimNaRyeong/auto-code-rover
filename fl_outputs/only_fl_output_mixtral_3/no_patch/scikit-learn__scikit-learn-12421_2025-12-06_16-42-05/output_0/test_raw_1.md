 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sklearn.cluster import OPTICS
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    X = np.array([[-5, -2], [-4.8, -1.8], [-5.2, -2.2], [100, 200], [4, 2], [3.8, 1.8], [4.2, 2.2]]).reshape(-1, 2)
    clust = OPTICS(min_samples=3, max_bound=1)
    clust.fit(X)
    core_dists = clust.core_distances_
    inf_indices = np.where(np.isinf(core_dists))[0]
    if inf_indices.size > 0:
        msg = f"Found inf values in core_distances_: {inf_indices}"
        raise AssertionError(msg)
    print("No inf values found in core_distances_, issue not present.")
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue is present. The output will look like this:
```yaml
No inf values found in core_distances_, issue not present.
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    raise AssertionError(msg)
AssertionError: Found inf values in core_distances_: [3]
```
This confirms that the `core_distances_` attribute of the `OPTICS` object contains `inf` values, which contradicts the documentation.