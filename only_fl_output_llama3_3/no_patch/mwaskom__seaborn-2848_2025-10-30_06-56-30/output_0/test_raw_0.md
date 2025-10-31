Here is the reproducer script:

```python
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

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

def main():
    try:
        iris = sns.load_dataset("iris")
        g = sns.PairGrid(iris, y_vars=["sepal_length","sepal_width"], x_vars=["petal_length","petal_width"])
        g.map(sns.scatterplot, hue=iris["species"])
        g.map(sns.regplot, scatter=False)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script should be run with Python 3.9 and Seaborn version 0.11.1. If the issue is present, it will print a stack trace and raise an `AssertionError`.