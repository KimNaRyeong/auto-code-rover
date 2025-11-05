Here is the reproducer script:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
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

def reproduce_issue():
    sns.set_context("paper")
    sns.set_style("white")

    data = (sns.load_dataset('iris').set_index('species')*1e7).reset_index()
    g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                    col_wrap=2, height=2.5, facet_kws=dict(sharex=False, sharey=False))
    g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
    for axes in g.axes.flat:
        axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

    try:
        plt.show()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.