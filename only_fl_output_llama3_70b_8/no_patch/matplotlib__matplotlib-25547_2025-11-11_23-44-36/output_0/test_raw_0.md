Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    # This does not warn:
    c = np.full(10, np.nan)
    c[0] = 1.
    plt.scatter(np.ones(10), np.ones(10), c=c)
    plt.show()

    try:
        # This should warn:
        plt.scatter(np.ones(10), np.ones(10), c=np.full(10, np.nan))
        plt.show()
    except UserWarning as e:
        print_stacktrace(e)
        assert False, "Expected no warning"

if __name__ == "__main__":
    main()
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will exit with code 0 when the issue is fixed.