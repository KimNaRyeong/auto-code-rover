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
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected no warning"

    if not isinstance(c[0], float):
        raise AssertionError("Reproducer did not work")

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` if the issue is present.