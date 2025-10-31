Here is the reproducer script:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import run_testsuite
import unittest
import sys
import traceback

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

def test_issue():
    try:
        sns.set()
        data = sns.load_dataset('iris')
        g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                        col_wrap=2)
        g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
        for axes in g.axes.flat:
            axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

        plt.draw()
        plt.show(block=False)
        plt.pause(1)  # wait for a second to see the plot
        plt.close()

        assert "Overlapping labels" not in str(plt.gcf().canvas.figure), \
            f"Expected no overlapping labels, but got: {str(plt.gcf().canvas.figure)}"

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    test_issue()
```

This script will run the test and check if the issue is present. If the issue is present, it will raise an `AssertionError` and print a stack trace of the error.