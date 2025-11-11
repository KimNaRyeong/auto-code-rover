Here is the reproducer script:

```python
import numpy as np
from matplotlib import pylab as plt

def main():
    try:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter([1,np.nan,3], [2,np.nan,4], [3, np.nan,5], color=[[.5,.5,.5,.5]]*3, s=11.5)
    except ValueError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.