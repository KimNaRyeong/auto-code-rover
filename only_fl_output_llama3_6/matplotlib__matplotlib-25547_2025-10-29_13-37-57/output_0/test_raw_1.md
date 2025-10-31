Here is the reproducer script:

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    c = np.full(10, np.nan)
    c[0] = 1.
    
    plt.scatter(np.ones(10), np.ones(10), c=c)
    
    try:
        plt.show()
    except UserWarning as e:
        print_stacktrace(e)
        assert False, "Expected no warning"
    else:
        print("Test passed")

if __name__ == "__main__":
    main()
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.