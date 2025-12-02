 I see, the issue is not easily reproducible in a standalone script. It seems to be related to the specific environment or configuration.

Here is an alternative approach to reproduce the issue:

1. Create a new virtual environment with the same Python version (3.9.12) and Matplotlib version (3.5.1) as the original environment.
2. Install the required packages: `conda install matplotlib numpy`.
3. Run the following script in the virtual environment:

```python
import matplotlib.pyplot as plt
import numpy as np

test = np.full((2, 1), -1)
plt.imshow(test)
plt.show()
```

4. If the issue is present, the script will raise a `ValueError: math domain error` when hovering the mouse over the plot.

Note: The script may not raise the error immediately, but only when hovering the mouse over the plot.

If this approach does not reproduce the issue, it may be related to the specific configuration or environment, and further investigation would be needed to determine the root cause.