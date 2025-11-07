Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from reproducer import print_stacktrace

def reproduce_issue():
    try:
        x = np.linspace(0, 10, 100)
        y = np.linspace(0, 10, 100)
        data = np.random.uniform(0, 50, (100, 100))
        
        plt.contour(x, y, data, levels=[100])
        print("Expected: [100]")
        print("Actual:", plt.contourf(x, y, data).levels)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to create a contour plot with the specified levels. If the issue is present and the levels are overridden by the autoscaling behavior, an `AssertionError` will be raised, and the stack trace will be printed.