Here is the reproducer script:

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    c = np.full(10, np.nan)

    try:
        plt.scatter(np.ones(10), np.ones(10), c=c)
        plt.show()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected no warning"

    c = np.full(10, np.nan)

    try:
        plt.scatter(np.ones(10), np.ones(10), c=c)
        plt.show()
    except UserWarning as e:
        print_stacktrace(e)
        assert True, "Expected warning"
    else:
        assert False, "Expected warning"

if __name__ == "__main__":
    main()
```

This script will run the two scatter plots and check if they raise an exception. If the first plot does not raise an exception but the second one does, then it means that the issue is present.