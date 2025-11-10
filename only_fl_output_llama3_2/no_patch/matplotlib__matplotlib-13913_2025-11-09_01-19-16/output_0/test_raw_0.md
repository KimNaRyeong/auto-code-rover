Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    c = np.arange(1000).astype(str)
    X = np.random.normal(0, 1, [1000, 2])

    try:
        assert all([matplotlib.colors.is_color_like(color) for color in c])
        plt.scatter(X[:, 0], X[:, 1], c=c)
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.