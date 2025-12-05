 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import seaborn as sns
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    iris = sns.load_dataset("iris")
    g = sns.PairGrid(iris, y_vars=["sepal_length","sepal_width"], x_vars=["petal_length","petal_width"])
    g.map(sns.scatterplot, hue=iris["species"])
    g.map(sns.regplot, scatter=False)
    plt.show()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        assert False
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace of the issue. The stack trace should show that the error occurs in the `scatterplot` function of the `seaborn` library.

To fix the issue, you can either use a previous version of `seaborn` (e.g. version 0.11.0), or use the `hue` keyword when creating the `PairGrid` object. For example, you can modify the `main` function as follows:
```python
def main():
    iris = sns.load_dataset("iris")
    g = sns.PairGrid(iris, y_vars=["sepal_length","sepal_width"], x_vars=["petal_length","petal_width"], hue=iris["species"])
    g.map(sns.scatterplot, hue=None)
    g.map(sns.regplot, scatter=False)
    plt.show()
```
This should produce the desired plot without any errors.